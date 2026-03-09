# Tableau Visualization Guide: Strategic Product Positioning

Since Tableau is a visual drag-and-drop software, it must be operated manually via the Tableau Desktop or Tableau Public interface. Follow this step-by-step guide to create the 8 requested visualizations, assemble them into an interactive dashboard, and present them in a 5-scene story using the `uploads/cleaned_retail_data_for_tableau.csv` dataset.

## Step 1: Connect to Data
1. Open Tableau (Desktop or Public).
2. Under "Connect", select **Text file**.
3. Navigate to your project folder and select `uploads/cleaned_retail_data_for_tableau.csv`.
4. Click **Sheet 1** at the bottom to begin creating visualizations.

---

## Step 2: Create the 8 Visualizations

### 1. Sales Volume by Product Position (Bar Chart)
*   **Columns**: `Product Position`
*   **Rows**: `SUM(Sales Volume)`
*   **Marks**: Drop `Product Position` on **Color**. 
*   **Labels**: Click the "T" (Label) icon on the toolbar to show values.
*   *Name the sheet: "Sales by Position"*

### 2. Sales Volume by Product Category (Pie Chart)
*   **Marks Type**: Change from Automatic to **Pie**.
*   **Marks**:
    *   Drop `Product Category` on **Color**.
    *   Drop `Sales Volume` on **Angle**.
    *   Drop `Product Category` and `SUM(Sales Volume)` on **Label**.
*   *Name the sheet: "Sales by Category"*

### 3. Price vs Competitor Price (Scatter Plot)
*   **Columns**: `AVG(Competitor Price)`
*   **Rows**: `AVG(Price)`
*   **Marks**: Drop `Product ID` on **Detail**. Drop `Product Category` on **Color**.
*   *Name the sheet: "Price vs Competitor"*

### 4. Promotion Impact on Sales (Side-by-Side Bar)
*   **Columns**: `Promotion`
*   **Rows**: `AVG(Sales Volume)`
*   **Marks**: Drop `Promotion` on **Color**.
*   *Name the sheet: "Promotion Impact"*

### 5. Foot Traffic vs Sales Volume (Box Plot or Bar)
*   **Columns**: `Foot Traffic`
*   **Rows**: `SUM(Sales Volume)`
*   **Marks**: Drop `Foot Traffic` on **Color**.
*   *Name the sheet: "Traffic vs Sales"*

### 6. Consumer Demographics Purchase Behavior (Tree Map)
*   **Marks**:
    *   Drop `Consumer Demographics` on **Color** and **Text**.
    *   Drop `SUM(Sales Volume)` on **Size** and **Text**.
*   *Name the sheet: "Demographics"*

### 7. Seasonal vs Non-Seasonal Sales (Line or Bar)
*   **Columns**: `Seasonal`
*   **Rows**: `SUM(Sales Volume)`
*   **Marks**: Drop `Product Category` on **Color** (to see the breakdown within seasonal).
*   *Name the sheet: "Seasonal Impact"*

### 8. Top 10 Highest Selling Products (Horizontal Bar)
*   **Columns**: `SUM(Sales Volume)`
*   **Rows**: `Product ID`
*   **Filter**: Drag `Product ID` to Filters -> Top -> By field -> Top 10 by Sales Volume (Sum).
*   **Sort**: Click the descending sort icon.
*   *Name the sheet: "Top 10 Products"*

---

## Step 3: Create the Interactive Dashboard
1. Click the **New Dashboard** icon at the bottom.
2. In the left pane, set the **Size** to "Automatic" or a fixed web resolution (e.g., 1200x800).
3. Drag the following sheets onto the dashboard canvas:
   *   *Sales by Position*
   *   *Sales by Category*
   *   *Promotion Impact*
   *   *Traffic vs Sales*
4. **Add Filters**:
   *   Click on any chart (e.g., *Sales by Category*).
   *   Click the dropdown arrow on the chart border -> **Filters** -> select `Product Category`.
   *   Repeat to add filters for `Consumer Demographics`, `Product Position`, `Promotion`, and `Seasonal`.
   *   For each filter card on the right, click its dropdown arrow -> **Apply to Worksheets** -> **All Using This Data Source**. This makes the dashboard fully interactive.
5. *Name the dashboard: "Strategic Overview Dashboard"*

---

## Step 4: Create the Data Story
1. Click the **New Story** icon at the bottom.
2. Set the Size to match your web layout.
3. **Scene 1 (Sales Overview)**:
   *   Drag the *Sales by Category* and *Top 10 Products* sheets.
   *   Caption: "Overall Sales Health across Categories"
4. **Scene 2 (Product Placement)**:
   *   Click "Blank" to add a new story point. Drag *Sales by Position*.
   *   Caption: "Aisle End-Caps drive the highest volume."
5. **Scene 3 (Promotion Effectiveness)**:
   *   New story point. Drag *Promotion Impact*.
   *   Caption: "Promoted items show a 30% aggregate lift."
6. **Scene 4 (Demographics)**:
   *   New story point. Drag *Demographics*.
   *   Caption: "Families dominate the high-traffic purchasing base."
7. **Scene 5 (Strategic Recommendations)**:
   *   New story point. Drag the *Price vs Competitor* scatter plot.
   *   Caption: "We have headroom to align pricing with competitors on high-visibility placements."

---

## Step 5: Embed in Flask Web App
1. Save your work to **Tableau Public** (File -> Save to Tableau Public).
2. Go to your dashboard on the Tableau Public website.
3. Click the **Share** icon at the bottom right of your visualization.
4. Copy the **Embed Code**.
5. Open `templates/dashboard.html` in your project folder, and replace the commented-out `<iframe>` placeholder with your embed code.
6. Repeat for the Story page: copy the embed code from your Story link and paste it into `templates/story.html`.
