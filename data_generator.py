import pandas as pd
import numpy as np
import random
import os

def generate_synthetic_data(num_records=1000):
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    product_categories = ['Clothing', 'Electronics', 'Food']
    product_positions = ['Aisle', 'End-cap', 'Front of Store']
    foot_traffic_levels = ['Low', 'Medium', 'High']
    demographics = ['Families', 'Seniors', 'Young Adults', 'College Students']

    data = {
        'Product ID': [f"PRD{str(i).zfill(4)}" for i in range(1, num_records + 1)],
        'Product Category': [random.choice(product_categories) for _ in range(num_records)],
        'Product Position': [random.choice(product_positions) for _ in range(num_records)],
        'Price': [round(random.uniform(5.0, 500.0), 2) for _ in range(num_records)],
        'Promotion': [random.choice(['Yes', 'No']) for _ in range(num_records)],
        'Foot Traffic': [random.choice(foot_traffic_levels) for _ in range(num_records)],
        'Consumer Demographics': [random.choice(demographics) for _ in range(num_records)],
        'Seasonal': [random.choice(['Yes', 'No']) for _ in range(num_records)]
    }

    df = pd.DataFrame(data)

    # Generate Competitor Price (slightly higher or lower than Price)
    df['Competitor Price'] = df['Price'] * np.random.uniform(0.85, 1.15, size=num_records)
    df['Competitor Price'] = df['Competitor Price'].round(2)

    # Generate Sales Volume based on some logical correlations
    sales_volume = []
    for index, row in df.iterrows():
        base_sales = np.random.normal(500, 150)
        
        # Boost sales based on certain factors
        if row['Product Position'] == 'End-cap':
            base_sales *= 1.4
        elif row['Product Position'] == 'Front of Store':
            base_sales *= 1.2
            
        if row['Promotion'] == 'Yes':
            base_sales *= 1.3
            
        if row['Foot Traffic'] == 'High':
            base_sales *= 1.5
        elif row['Foot Traffic'] == 'Low':
            base_sales *= 0.7
            
        if row['Price'] < row['Competitor Price']:
            base_sales *= 1.1
            
        # Ensure positive sales integer
        sales = max(10, int(base_sales))
        sales_volume.append(sales)

    df['Sales Volume'] = sales_volume

    # Add some deliberate missing values for testing the cleaning pipeline
    df.loc[df.sample(int(num_records * 0.05)).index, 'Price'] = np.nan
    df.loc[df.sample(int(num_records * 0.05)).index, 'Promotion'] = np.nan

    return df

if __name__ == "__main__":
    print("Generating synthetic retail dataset...")
    df = generate_synthetic_data(1500)
    
    # Ensure uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    
    file_path = 'uploads/raw_retail_data.csv'
    df.to_csv(file_path, index=False)
    print(f"Dataset generated and saved to {file_path}")
