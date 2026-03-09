import os
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pipeline import process_data
from visualizations import generate_dashboard_charts, generate_story_charts

app = Flask(__name__)
app.secret_key = 'super_secret_strategic_key'

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DB_PATH = 'sales_data.db'

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the newly uploaded file through the pipeline
            df = process_data(filepath)
            if df is not None:
                flash(f'File {filename} successfully uploaded, cleaned, and stored in the database!')
                return redirect(url_for('overview'))
            else:
                flash('Error processing the dataset.')
                return redirect(request.url)
        else:
            flash('Invalid file format. Please upload a CSV file.')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/overview')
def overview():
    try:
        conn = get_db_connection()
        # Fetch top 100 rows for preview
        data = conn.execute('SELECT * FROM retail_sales LIMIT 100').fetchall()
        # Get total count
        total_records = conn.execute('SELECT COUNT(*) FROM retail_sales').fetchone()[0]
        conn.close()
        
        # Get column names dynamically if data exists
        columns = data[0].keys() if data else []
        return render_template('overview.html', data=data, columns=columns, total_records=total_records)
    except sqlite3.OperationalError:
        flash('Database not found or empty. Please upload a dataset first.')
        return redirect(url_for('upload_file'))

@app.route('/dashboard')
def dashboard():
    charts = generate_dashboard_charts()
    if charts is None:
        flash('Run the data pipeline first to generate visualizations.')
        return redirect(url_for('upload_file'))
    return render_template('dashboard.html', charts=charts)

@app.route('/story')
def story():
    charts = generate_story_charts()
    if charts is None:
        flash('Run the data pipeline first to generate the story.')
        return redirect(url_for('upload_file'))
    return render_template('story.html', charts=charts)

@app.route('/insights')
def insights():
    try:
        conn = get_db_connection()
        
        # 1. Best performing product position
        position_sales = conn.execute('''
            SELECT "Product Position", SUM("Sales Volume") as total_sales 
            FROM retail_sales 
            GROUP BY "Product Position" 
            ORDER BY total_sales DESC LIMIT 1
        ''').fetchone()
        
        # 2. Demographic group purchasing the most
        demo_sales = conn.execute('''
            SELECT "Consumer Demographics", SUM("Sales Volume") as total_sales 
            FROM retail_sales 
            GROUP BY "Consumer Demographics" 
            ORDER BY total_sales DESC LIMIT 1
        ''').fetchone()
        
        # 3. Impact of promotions on sales (Average sales volume Promoted vs Not Promoted)
        promo_impact = conn.execute('''
            SELECT "Promotion", AVG("Sales Volume") as avg_sales 
            FROM retail_sales 
            GROUP BY "Promotion"
        ''').fetchall()
        
        # 4. Best performing product category
        category_sales = conn.execute('''
            SELECT "Product Category", SUM("Sales Volume") as total_sales 
            FROM retail_sales 
            GROUP BY "Product Category" 
            ORDER BY total_sales DESC LIMIT 1
        ''').fetchone()
        
        # 5. Price difference impact on sales (Correlation proxy: does positive difference equal more sales?)
        # Simple aggregated view: average sales when cheaper than competitor vs average sales when more expensive
        price_diff_impact = conn.execute('''
            SELECT 
                CASE WHEN "Price Difference" < 0 THEN 'Cheaper than Competitor'
                     ELSE 'More Expensive than Competitor' END as price_status,
                AVG("Sales Volume") as avg_sales
            FROM retail_sales
            GROUP BY price_status
        ''').fetchall()

        conn.close()
        
        return render_template('insights.html', 
                               position_sales=position_sales, 
                               demo_sales=demo_sales, 
                               promo_impact=promo_impact, 
                               category_sales=category_sales,
                               price_diff_impact=price_diff_impact)
    except sqlite3.OperationalError:
        flash('Run the data pipeline first to generate insights.')
        return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
