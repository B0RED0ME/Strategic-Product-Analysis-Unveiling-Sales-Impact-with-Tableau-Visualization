import pandas as pd
import sqlite3
import os

def process_data(csv_file_path):
    print(f"Processing dataset: {csv_file_path}")
    
    # 1. IMPORT DATA
    try:
        df = pd.read_csv(csv_file_path)
        print("Data imported successfully.")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

    # 2. DATA CLEANING
    print("Cleaning data...")
    # Handle missing values: 
    # Fill numeric columns with median, categorical with mode
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    categorical_cols = df.select_dtypes(exclude=['number']).columns
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Convert Categorical/Boolean string fields
    # Using explicit True/False or keeping them as categorical depending on mapping need.
    # In pandas, working with standard boolean types is cleaner.
    df['Promotion'] = df['Promotion'].map({'Yes': True, 'No': False}).astype(bool)
    df['Seasonal'] = df['Seasonal'].map({'Yes': True, 'No': False}).astype(bool)
    
    # Ensure Categories
    df['Foot Traffic'] = df['Foot Traffic'].astype('category')
    df['Product Position'] = df['Product Position'].astype('category')
    
    # 3. FEATURE ENGINEERING
    print("Engineering custom features...")
    # Price Difference = Price - Competitor Price
    df['Price Difference'] = (df['Price'] - df['Competitor Price']).round(2)
    
    # For Promotion Impact (we simply calculate the group mean later, but we can flag it here)
    # Traffic Conversion Rate = Sales Volume / Traffic Level Weight (pseudo conversion logic)
    traffic_weights = {'Low': 1, 'Medium': 2, 'High': 3}
    df['Traffic Weight'] = df['Foot Traffic'].map(traffic_weights).astype(int)
    df['Traffic Conversion Index'] = (df['Sales Volume'] / df['Traffic Weight']).round(2)
    
    # 4. EXPORT TO SQLITE
    print("Storing data in SQLite database...")
    db_path = 'sales_data.db'
    conn = sqlite3.connect(db_path)
    
    # Store processed DataFrame to SQL table
    df.to_sql('retail_sales', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data successfully stored in SQLite database: {db_path}")

    # 5. EXPORT CLEANED CSV FOR TABLEAU
    clean_csv_path = 'uploads/cleaned_retail_data_for_tableau.csv'
    df.to_csv(clean_csv_path, index=False)
    print(f"Cleaned data exported for Tableau at: {clean_csv_path}")
    
    return df

if __name__ == "__main__":
    # If run directly as a script, process the raw data generated earlier
    raw_file = 'uploads/raw_retail_data.csv'
    if os.path.exists(raw_file):
        process_data(raw_file)
    else:
        print(f"Raw file {raw_file} not found. Please run data_generator.py first.")
