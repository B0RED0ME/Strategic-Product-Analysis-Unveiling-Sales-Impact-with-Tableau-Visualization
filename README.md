# Strategic Product Positioning Analysis System

A comprehensive project analyzing the complex relationship between product positioning, pricing strategy, consumer demographics, and sales performance in retail environments.

## Architecture Versions

This repository contains two completely separate deployment architectures for the same project depending on your hosting requirements:

### 1. Static Web Application (GitHub Pages)
The primary layout found in the root directory (`index.html`, `dashboard.html`, `story.html`) serves as a completely static, zero-configuration website.
* **Tech Stack**: HTML5, CSS3, Bootstrap 5, Javascript, Plotly.js.
* **Visuals**: Designed to render previously exported Plotly charts natively on the client without executing any Python backend servers.
* **Deployment**: Simply push this repository to GitHub and enable **GitHub Pages** from the repository settings! It will automatically map your `index.html` to a public URL.

### 2. Streamlit Dynamic Platform
For users requiring real-time Python execution and interactive Plotly charting, the `streamlit_app.py` file contains the full stack application.
* **Tech Stack**: Python, Streamlit, Plotly, Pandas, SQLite.
* **Visuals**: Uses Python natively to build real-time interactive charts bypassing Tableau entirely.
* **Deployment**: Connect your GitHub repository directly to [Streamlit Community Cloud](https://share.streamlit.io).

## GitHub Pages Setup Instructions

1. **Update Data (Optional)**: If you've modified your CSV or SQLite database, you need to export the latest interactive charts to a static Javascript structure first:
```bash
python export_static_charts.py
```
*(This writes the graphs natively to `js/charts.js`)*

2. Push your repository to GitHub:
```bash
git init
git add .
git commit -m "Initial Deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```
3. Navigate to your repository on GitHub.
4. Click on **Settings** > **Pages** (on the left sidebar).
5. Under **Build and deployment**, select **Deploy from a branch**.
6. Select the `main` branch and `/ (root)` folder, then click **Save**.
7. Wait 1-2 minutes, and your fully interactive static-site will be live at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`
