import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px
from pipeline import process_data

# Page Config
st.set_page_config(page_title="Strategic Product Positioning", page_icon="📈", layout="wide")

DB_PATH = 'sales_data.db'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to get data
@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM retail_sales", conn)
        conn.close()
        return df
    except sqlite3.OperationalError:
        return None

# Custom CSS for aesthetics
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #4361ee;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio("Go to", [
    "Home", 
    "Data Upload", 
    "Data Overview", 
    "Interactive Dashboard", 
    "Data Story", 
    "Strategic Insights"
])

st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ using Streamlit & Plotly")

# --- 1. HOME ---
if page == "Home":
    st.title("📈 Strategic Product Positioning Analysis")
    st.markdown("### Redefining Retail Strategy")
    st.write("Unlock hidden insights in your sales data. Optimize product placement and maximize revenue with AI-driven analytics.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Data Integration**\n\nUpload sales and store data. Automatically clean and engineer features.")
    with col2:
        st.success("**Advanced Visualizations**\n\nLeverage Plotly dashboards to visualize complex relationships.")
    with col3:
        st.warning("**Actionable Insights**\n\nDiscover data-driven recommendations that impact your bottom line.")

# --- 2. DATA UPLOAD ---
elif page == "Data Upload":
    st.title("📤 Upload Dataset")
    st.write("Import your CSV dataset to begin the strategic analysis.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        if st.button("Process Dataset"):
            with st.spinner("Uploading and running data pipeline..."):
                filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Run the backend pipeline
                df = process_data(filepath)
                if df is not None:
                    st.success("File successfully uploaded, cleaned, and stored in the database!")
                    st.cache_data.clear() # Clear cache to load new data
                else:
                    st.error("Error processing the dataset.")

# --- 3. DATA OVERVIEW ---
elif page == "Data Overview":
    st.title("🗄️ Database Overview")
    df = load_data()
    
    if df is not None:
        st.metric("Total Records", f"{len(df):,}")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("Database not found or empty. Please upload a dataset first.")

# --- 4. INTERACTIVE DASHBOARD ---
elif page == "Interactive Dashboard":
    st.title("📊 Executive Dashboard")
    df = load_data()
    
    if df is not None:
        st.markdown("### Key Value Drivers")
        col1, col2 = st.columns(2)
        with col1:
            position_sales = df.groupby('Product Position')['Sales Volume'].sum().reset_index()
            fig1 = px.bar(position_sales, x='Product Position', y='Sales Volume', title='Sales by Product Position', color='Product Position')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            category_sales = df.groupby('Product Category')['Sales Volume'].sum().reset_index()
            fig2 = px.pie(category_sales, names='Product Category', values='Sales Volume', title='Sales by Category', hole=0.3)
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown("---")
        st.markdown("### Environment & Demographics")
        col3, col4 = st.columns(2)
        with col3:
            demo_sales = df.groupby('Consumer Demographics')['Sales Volume'].sum().reset_index()
            fig6 = px.bar(demo_sales, x='Consumer Demographics', y='Sales Volume', title='Sales by Consumer Demographics', color='Consumer Demographics')
            st.plotly_chart(fig6, use_container_width=True)
        with col4:
            fig5 = px.box(df, x='Foot Traffic', y='Sales Volume', color='Foot Traffic', title='Foot Traffic Impact on Sales')
            st.plotly_chart(fig5, use_container_width=True)

        st.markdown("---")
        st.markdown("### Pricing & Tactics")
        col5, col6 = st.columns(2)
        with col5:
            promo_sales = df.groupby('Promotion')['Sales Volume'].mean().reset_index()
            promo_sales['Promotion'] = promo_sales['Promotion'].apply(lambda x: 'Yes' if x else 'No')
            fig4 = px.bar(promo_sales, x='Promotion', y='Sales Volume', title='Average Sales by Promotion Status', color='Promotion')
            st.plotly_chart(fig4, use_container_width=True)
        with col6:
            fig3 = px.scatter(df, x='Competitor Price', y='Price', color='Product Category', title='Price vs Competitor Price', hover_data=['Product ID'])
            st.plotly_chart(fig3, use_container_width=True)
            
        st.markdown("---")
        st.markdown("### Performance & Seasonality")
        col7, col8 = st.columns(2)
        with col7:
            seasonal_sales = df.groupby('Seasonal')['Sales Volume'].sum().reset_index()
            seasonal_sales['Seasonal'] = seasonal_sales['Seasonal'].apply(lambda x: 'Yes' if x else 'No')
            fig7 = px.bar(seasonal_sales, x='Seasonal', y='Sales Volume', title='Sales: Seasonal vs Non-Seasonal', color='Seasonal')
            st.plotly_chart(fig7, use_container_width=True)
        with col8:
            top10 = df.groupby('Product ID')['Sales Volume'].sum().reset_index().nlargest(10, 'Sales Volume')
            fig8 = px.bar(top10, x='Sales Volume', y='Product ID', orientation='h', title='Top 10 Products by Sales Volume').update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig8, use_container_width=True)
    else:
         st.error("Please process a dataset first.")

# --- 5. DATA STORY ---
elif page == "Data Story":
    st.title("📖 Strategic Story")
    df = load_data()
    
    if df is not None:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "1. Sales Overview", "2. Placement Impact", "3. Promotion Effectiveness", "4. Demographics", "5. Recommendations"
        ])
        
        with tab1:
            st.subheader("Overall Sales Health")
            st.write("Understanding our core product categories and top movers provides the baseline for strategic optimization.")
            category_sales = df.groupby('Product Category')['Sales Volume'].sum().reset_index()
            st.plotly_chart(px.pie(category_sales, names='Product Category', values='Sales Volume', title='Sales by Category', hole=0.3), use_container_width=True)
            st.info("💡 **Takeaway:** Focus inventory expansion on the categories claiming the largest slice of the pie.")
            
        with tab2:
            st.subheader("The Power of Placement")
            st.write("Where a product sits in the store radically influences its velocity.")
            position_sales = df.groupby('Product Position')['Sales Volume'].sum().reset_index()
            st.plotly_chart(px.bar(position_sales, x='Product Position', y='Sales Volume', title='Sales by Product Position', color='Product Position'), use_container_width=True)
            st.success("💡 **Takeaway:** End-caps drive substantially higher volume than standard aisles.")
            
        with tab3:
            st.subheader("Promotion Effectiveness")
            st.write("Do active promotions actually yield higher volume, and at what cost?")
            promo_sales = df.groupby('Promotion')['Sales Volume'].mean().reset_index()
            promo_sales['Promotion'] = promo_sales['Promotion'].apply(lambda x: 'Yes' if x else 'No')
            st.plotly_chart(px.bar(promo_sales, x='Promotion', y='Sales Volume', title='Average Sales by Promotion Status', color='Promotion'), use_container_width=True)
            st.warning("💡 **Takeaway:** Promoted items show clear lift. The key is applying promos selectively to high-margin goods.")
            
        with tab4:
            st.subheader("Who is Buying?")
            st.write("Demographic analysis reveals which segments are responsible for the highest sales volume.")
            demo_sales = df.groupby('Consumer Demographics')['Sales Volume'].sum().reset_index()
            st.plotly_chart(px.bar(demo_sales, x='Consumer Demographics', y='Sales Volume', title='Sales by Consumer Demographics', color='Consumer Demographics'), use_container_width=True)
            st.info("💡 **Takeaway:** Tailor store front aesthetics to the dominant purchasing demographic identified here.")
            
        with tab5:
            st.subheader("Pricing Elasticity")
            st.write("Pricing elasticity is the final lever. Comparing our prices to competitors gives us maneuvering room.")
            st.plotly_chart(px.scatter(df, x='Competitor Price', y='Price', color='Product Category', title='Price vs Competitor Price', hover_data=['Product ID']), use_container_width=True)
            st.error("💡 **Takeaway:** We can closely align high-visibility placements with competitor pricing.")
    else:
        st.error("Please process a dataset first.")

# --- 6. STRATEGIC INSIGHTS ---
elif page == "Strategic Insights":
    st.title("💡 Dynamic Database Insights")
    st.write("These insights are automatically generated from your current SQLite database showing the relationships within your retail data.")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        
        position_sales = conn.execute('SELECT "Product Position", SUM("Sales Volume") as total_sales FROM retail_sales GROUP BY "Product Position" ORDER BY total_sales DESC LIMIT 1').fetchone()
        demo_sales = conn.execute('SELECT "Consumer Demographics", SUM("Sales Volume") as total_sales FROM retail_sales GROUP BY "Consumer Demographics" ORDER BY total_sales DESC LIMIT 1').fetchone()
        category_sales = conn.execute('SELECT "Product Category", SUM("Sales Volume") as total_sales FROM retail_sales GROUP BY "Product Category" ORDER BY total_sales DESC LIMIT 1').fetchone()
        
        conn.close()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #4361ee;">
                <p style="color: grey; font-size: 14px; margin-bottom: 0;">Highest Sales Generator</p>
                <h3 style="margin-top: 0;">Best Position: {position_sales['Product Position']}</h3>
                <p>Driving a total volume of <b>{position_sales['total_sales']:,}</b> units.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #f72585;">
                <p style="color: grey; font-size: 14px; margin-bottom: 0;">Top Performer</p>
                <h3 style="margin-top: 0;">Best Category: {category_sales['Product Category']}</h3>
                <p>Yielding an impressive total sales volume of <b>{category_sales['total_sales']:,}</b> units.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #4cc9f0;">
                <p style="color: grey; font-size: 14px; margin-bottom: 0;">Primary Consumers</p>
                <h3 style="margin-top: 0;">Top Demo: {demo_sales['Consumer Demographics']}</h3>
                <p>Total purchase volume of <b>{demo_sales['total_sales']:,}</b> units.</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### Strategic Business Recommendations")
        st.markdown("""
        1. **Implement dynamic pricing:** Bundle offers for products placed in low-traffic aisles to offset lower visibility.
        2. **Rotate high-margin priority products:** Move them into end-cap positions on a bi-weekly schedule to maximize the traffic multipliers identified in the DB analysis.
        3. **Ensure high inventory levels:** Target the top-performing demographic product lines during identified peak seasonal windows.
        """)

    except Exception as e:
        st.error("Please run the data pipeline first to generate insights.")
