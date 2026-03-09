import sqlite3
import pandas as pd
import json
import plotly
import plotly.express as px

DB_PATH = 'sales_data.db'

def get_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM retail_sales", conn)
        conn.close()
        return df
    except sqlite3.OperationalError:
        return None

def generate_dashboard_charts():
    df = get_data()
    if df is None or df.empty:
        return None

    charts = {}

    # 1. Sales Volume by Product Position (Bar)
    position_sales = df.groupby('Product Position')['Sales Volume'].sum().reset_index()
    fig1 = px.bar(position_sales, x='Product Position', y='Sales Volume', title='Sales by Product Position', color='Product Position')
    charts['sales_by_position'] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # 2. Sales Volume by Product Category (Pie)
    category_sales = df.groupby('Product Category')['Sales Volume'].sum().reset_index()
    fig2 = px.pie(category_sales, names='Product Category', values='Sales Volume', title='Sales by Category', hole=0.3)
    charts['sales_by_category'] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # 3. Price vs Competitor Price (Scatter)
    fig3 = px.scatter(df, x='Competitor Price', y='Price', color='Product Category', title='Price vs Competitor Price', hover_data=['Product ID'])
    charts['price_vs_competitor'] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    # 4. Promotion Impact on Sales (Bar)
    promo_sales = df.groupby('Promotion')['Sales Volume'].mean().reset_index()
    promo_sales['Promotion'] = promo_sales['Promotion'].apply(lambda x: 'Yes' if x else 'No')
    fig4 = px.bar(promo_sales, x='Promotion', y='Sales Volume', title='Average Sales by Promotion Status', color='Promotion')
    charts['promotion_impact'] = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    # 5. Foot Traffic vs Sales Volume (Box)
    fig5 = px.box(df, x='Foot Traffic', y='Sales Volume', color='Foot Traffic', title='Foot Traffic Impact on Sales')
    charts['traffic_impact'] = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

    # 6. Consumer Demographics Purchase Behavior (Bar)
    demo_sales = df.groupby('Consumer Demographics')['Sales Volume'].sum().reset_index()
    fig6 = px.bar(demo_sales, x='Consumer Demographics', y='Sales Volume', title='Sales by Consumer Demographics', color='Consumer Demographics')
    charts['demographics'] = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

    # 7. Seasonal vs Non-Seasonal Sales (Bar)
    seasonal_sales = df.groupby('Seasonal')['Sales Volume'].sum().reset_index()
    seasonal_sales['Seasonal'] = seasonal_sales['Seasonal'].apply(lambda x: 'Yes' if x else 'No')
    fig7 = px.bar(seasonal_sales, x='Seasonal', y='Sales Volume', title='Sales: Seasonal vs Non-Seasonal', color='Seasonal')
    charts['seasonal'] = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)

    # 8. Top 10 Highest Selling Products (Horizontal Bar)
    top10 = df.groupby('Product ID')['Sales Volume'].sum().reset_index().nlargest(10, 'Sales Volume')
    fig8 = px.bar(top10, x='Sales Volume', y='Product ID', orientation='h', title='Top 10 Products by Sales Volume').update_yaxes(categoryorder="total ascending")
    charts['top_10'] = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)

    return charts

def generate_story_charts():
    # We can reuse the same functions and structure them for the story scenes
    charts = generate_dashboard_charts()
    return charts
