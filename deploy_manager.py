import streamlit as st
from github import Github
import os
import subprocess
import shutil
import time
import sys
import psutil
import json

# Setup page
st.set_page_config(page_title="Auto-Deploy Platform", page_icon="🚀", layout="wide")

# Directory to store cloned repos
DEPLOY_DIR = os.path.join(os.getcwd(), 'deployments')
os.makedirs(DEPLOY_DIR, exist_ok=True)
STATE_FILE = os.path.join(DEPLOY_DIR, 'deploy_state.json')

# Initialize session state
if 'github_token' not in st.session_state:
    st.session_state.github_token = ""
if 'repos' not in st.session_state:
    st.session_state.repos = []
if 'selected_repo' not in st.session_state:
    st.session_state.selected_repo = None
if 'deployments' not in st.session_state:
    st.session_state.deployments = {}

# Load stored deployments
def load_deploy_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                
                # Verify processes are still running
                active_deployments = {}
                for repo, info in state.items():
                    pid = info.get('pid')
                    if pid and psutil.pid_exists(pid):
                        active_deployments[repo] = info
                
                st.session_state.deployments = active_deployments
                save_deploy_state()
        except:
            pass

def save_deploy_state():
    with open(STATE_FILE, 'w') as f:
        json.dump(st.session_state.deployments, f)

load_deploy_state()

# --- Functions ---

def detect_project_type(repo_path):
    files = os.listdir(repo_path)
    content = ""
    req_path = os.path.join(repo_path, 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
    
    # 1. Streamlit
    if 'streamlit' in content or any(f.endswith('.py') and 'streamlit' in open(os.path.join(repo_path, f), 'r', encoding='utf-8', errors='ignore').read() for f in files if f.endswith('.py')):
        # find main file
        main_file = 'streamlit_app.py' if 'streamlit_app.py' in files else 'app.py'
        return 'Streamlit', f"streamlit run {main_file} --server.port 8502"
    
    # 2. FastAPI
    if 'fastapi' in content:
        main_file = 'main:app' if 'main.py' in files else 'app:app'
        return 'FastAPI', f"uvicorn {main_file} --host 0.0.0.0 --port 8000"
    
    # 3. Flask
    if 'flask' in content or any(f.endswith('.py') and 'Flask(__name__)' in open(os.path.join(repo_path, f), 'r', encoding='utf-8', errors='ignore').read() for f in files if f.endswith('.py')):
        main_file = 'app.py' if 'app.py' in files else 'main.py'
        return 'Flask', f"python {main_file}"
    
    # 4. Node.js
    if 'package.json' in files:
        return 'Node.js', "npm start"
    
    # 5. Static HTML
    if 'index.html' in files:
        return 'Static Website', "python -m http.server 8080"
    
    return 'Unknown', None

def deploy_repository(repo):
    st.info(f"Starting deployment for {repo.name}...")
    repo_path = os.path.join(DEPLOY_DIR, repo.name)
    
    # 1. Clone repository
    if os.path.exists(repo_path):
        st.write("Cleaning previous build directory...")
        shutil.rmtree(repo_path, ignore_errors=True)
    
    st.write("Cloning repository from GitHub...")
    clone_url = repo.clone_url.replace("https://", f"https://{st.session_state.github_token}@")
    clone_cmd = f"git clone {clone_url} {repo_path}"
    subprocess.run(clone_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    st.success("Repository cloned locally.")
    
    # 2. Architecture Detection
    st.write("Detecting project architecture...")
    proj_type, start_cmd = detect_project_type(repo_path)
    st.write(f"Detected project type: **{proj_type}**")
    
    if proj_type == 'Unknown':
        st.error("Could not determine project architecture (Missing app.py, requirements.txt, or package.json).")
        return False
        
    # 3. Install Dependencies
    st.write("Installing dependencies... This may take a minute.")
    log_file_path = os.path.join(repo_path, 'deploy.log')
    with open(log_file_path, 'w') as log_file:
        if os.path.exists(os.path.join(repo_path, 'requirements.txt')):
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=repo_path, stdout=log_file, stderr=log_file)
        elif os.path.exists(os.path.join(repo_path, 'package.json')):
            subprocess.run("npm install", shell=True, cwd=repo_path, stdout=log_file, stderr=log_file)
    st.success("Dependencies installed.")
    
    # 4. Start Server
    st.write("Starting application server...")
    with open(log_file_path, 'a') as log_file:
        process = subprocess.Popen(start_cmd, shell=True, cwd=repo_path, stdout=log_file, stderr=log_file)
    
    # Save State
    port = "8502" if proj_type == 'Streamlit' else ("8000" if proj_type == 'FastAPI' else ("8080" if proj_type == 'Static Website' else "5000"))
    link = f"http://localhost:{port}"
    
    st.session_state.deployments[repo.name] = {
        'type': proj_type,
        'pid': process.pid,
        'path': repo_path,
        'link': link,
        'cmd': start_cmd,
        'log_file': log_file_path,
        'status': 'Running 🟢'
    }
    save_deploy_state()
    st.success(f"Deployment successful! App is running at {link}")
    return True


st.title("🚀 PaaS: Automated GitHub Deployment Platform")
st.markdown("Deploy your Streamlit, Flask, FastAPI, or Node projects directly from your GitHub repositories with zero configuration.")

# Sidebar - Settings & Authentication
st.sidebar.header("🔑 GitHub Authentication")
token_input = st.sidebar.text_input("Personal Access Token (PAT)", type="password", value=st.session_state.github_token)
if st.sidebar.button("Connect via OAuth / PAT"):
    if token_input:
        st.session_state.github_token = token_input
        try:
            g = Github(token_input)
            user = g.get_user()
            st.sidebar.success(f"Connected as: {user.login}")
            # Fetch repos
            repos = list(user.get_repos(sort="updated"))
            st.session_state.repos = [r for r in repos if not r.fork]
            st.rerun()
        except Exception as e:
            st.sidebar.error("Authentication failed. Invalid Token.")
    else:
        st.sidebar.warning("Please enter a token.")

# Main Dashboard
tab1, tab2 = st.tabs(["📦 New Deployment", "🖥️ Active Deployments Dashboard"])

# TAB 1: New Deployment
with tab1:
    if st.session_state.repos:
        st.subheader("Select a Repository to Deploy")
        repo_names = [r.name for r in st.session_state.repos]
        selected_repo_name = st.selectbox("Your Repositories", repo_names)
        
        selected_repo = next((r for r in st.session_state.repos if r.name == selected_repo_name), None)
        
        if selected_repo:
            st.markdown(f"**Description:** {selected_repo.description or 'No description'}")
            st.markdown(f"**Default Branch:** `{selected_repo.default_branch}`")
            st.markdown(f"**Language:** {selected_repo.language}")
            
            if selected_repo.name in st.session_state.deployments:
                st.warning(f"⚠️ **{selected_repo.name}** is already actively deployed.")
                
            if st.button("🚀 Deploy Application", type="primary"):
                with st.status(f"Deploying {selected_repo.name}...", expanded=True) as status:
                    success = deploy_repository(selected_repo)
                    if success:
                        status.update(label="Deployment Complete!", state="complete", expanded=False)
                        st.balloons()
                    else:
                        status.update(label="Deployment Failed.", state="error")
    else:
        st.info("Connect your GitHub account in the sidebar to fetch your repositories.")

# TAB 2: Active Dashboard
with tab2:
    st.subheader("Active Environments")
    if not st.session_state.deployments:
        st.write("No active deployments.")
    else:
        for repo_name, info in list(st.session_state.deployments.items()):
            pid = info.get('pid')
            is_alive = psutil.pid_exists(pid) if pid else False
            status_icon = "🟢 Running" if is_alive else "🔴 Stopped/Failed"
            
            with st.expander(f"{repo_name} - {status_icon}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Project Type:** {info['type']}")
                    st.markdown(f"**Live Link:** [Click to open Application]({info['link']})")
                    st.markdown(f"**Command:** `{info['cmd']}`")
                    st.markdown(f"**Process ID:** `{pid}`")
                
                with col2:
                    if is_alive:
                        if st.button(f"🛑 Stop Output", key=f"stop_{repo_name}"):
                            try:
                                parent = psutil.Process(pid)
                                for child in parent.children(recursive=True):
                                    child.terminate()
                                parent.terminate()
                                st.session_state.deployments[repo_name]['status'] = 'Stopped 🔴'
                                save_deploy_state()
                                st.rerun()
                            except:
                                pass
                    else:
                        if st.button(f"🗑️ Remove from Dashboard", key=f"rm_{repo_name}"):
                            del st.session_state.deployments[repo_name]
                            save_deploy_state()
                            st.rerun()

                st.markdown("#### Build / Server Logs")
                try:
                    with open(info['log_file'], 'r') as f:
                        lines = f.readlines()
                        last_lines = "".join(lines[-20:])
                        st.code(last_lines, language="bash")
                except:
                    st.code("Logs not available.", language="bash")
