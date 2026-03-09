import json
import os
from visualizations import generate_dashboard_charts

def export_charts_to_js():
    print("Generating charts from database...")
    charts = generate_dashboard_charts()
    
    if charts is None:
        print("Error: No data in database to generate charts.")
        return

    # Ensure js directory exists
    os.makedirs('js', exist_ok=True)
    
    js_content = "const chartData = {\n"
    for key, val in charts.items():
        js_content += f"    {key}: {val},\n"
    js_content += "};\n"
    
    js_path = os.path.join('js', 'charts.js')
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Successfully exported charts to {js_path}")

if __name__ == "__main__":
    export_charts_to_js()
