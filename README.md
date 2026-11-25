# E-Commerce Product Funnel & Basket Analysis

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Data%20Visualization-blue?logo=python)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Project Overview
This repository contains the complete analytical framework, relational database queries, association rule mining scripts, and interactive dashboards developed to analyze customer conversion journeys and cross-selling purchase affinities across **30,000+ customer sessions** and **7,400+ completed orders**.

By extracting and joining multi-table transaction and clickstream records in MySQL, the project isolated a critical **18% abandonment drop-off between Cart and Checkout**. To recover this drop-off and elevate basket profitability, Market Basket Analysis was performed in Python using the Apriori algorithm, formulating data-backed bundle recommendations to improve Average Order Value (AOV).

---

## 🚀 Key Highlights & Resume Alignments
- **Conversion Journey & Funnel Tracking**: Extracted and joined multi-table session clickstream logs in MySQL to track users through 5 stages: Home Page -> Product View -> Add to Cart -> Initiate Checkout -> Complete Purchase.
- **18% Abandonment Drop-off Identified**: Isolated an 18.0% drop-off between cart addition and checkout initiation, with mobile devices showing the highest friction (21.2% abandonment).
- **Market Basket Analysis (MBA)**: Implemented the Apriori algorithm in Python (`mlxtend`) to evaluate frequent itemsets across thousands of completed order baskets, discovering strong co-purchasing affinities with lift values up to **3.12x**.
- **Cross-Selling Bundles**: Formulated strategic "Frequently Bought Together" bundles to improve Average Order Value (AOV) by an estimated **14.5%**.
- **Data Visualizations**: Built custom high-resolution conversion funnel diagrams, device drop-off charts, hourly conversion trends, and affinity heatmaps using Seaborn and Matplotlib.

---

## 📂 Repository Structure
```
Ecommerce-Product-Funnel-Basket-Analysis/
├── data/
│   ├── funnel_events.csv                      # 65,000+ session clickstream events
│   ├── orders.csv                             # Order headers with timestamps and totals
│   ├── order_items.csv                        # Line-item level basket contents
│   └── products.csv                           # Product catalog with prices and categories
├── sql/
│   ├── 01_ecommerce_schema.sql                # Multi-table MySQL DDL with indexes
│   ├── 02_funnel_dropoff_analysis.sql         # CTEs, LAG() window functions, drop-off queries
│   └── 03_basket_and_order_kpis.sql           # Self-joins for co-occurrence and basket KPIs
├── scripts/
│   ├── generate_ecommerce_data.py             # Clickstream and basket data generation engine
│   ├── funnel_analysis.py                     # Conversion journey computation and Matplotlib funnels
│   └── market_basket_analysis.py              # Apriori algorithm, lift scores, Seaborn heatmaps
├── visualizations/
│   ├── conversion_funnel.png                  # High-res visual conversion funnel diagram
│   ├── device_conversion_comparison.png       # Mobile vs Desktop vs Tablet drop-off
│   ├── hourly_conversion_trends.png          # 24-hour conversion trajectory
│   ├── market_basket_affinity_heatmap.png     # Co-purchasing correlation matrix
│   └── top_cross_sell_bundles.png             # Top bundle lift score comparisons
├── reports/
│   ├── funnel_and_basket_actionable_insights.md # Full business insights and recommendations
│   └── bundle_cross_sell_recommendations.csv  # Ranked cross-selling bundles
├── dashboard/
│   └── app.py                                 # Interactive Streamlit Funnel & Basket Explorer
└── README.md                                  # Complete project documentation
```

---

## 🛠️ Tech Stack & Methodologies
- **Databases & Querying**: MySQL 8.0, CTEs (Common Table Expressions), Window Functions (`LAG()`, `FIRST_VALUE()`), Self-Joins for Co-occurrence.
- **Machine Learning & Cheminformatics/Mining**: Apriori Algorithm, Association Rule Mining, Support, Confidence, Lift, Leverage (`mlxtend.frequent_patterns`).
- **Data Analysis & Visualization**: Python 3.11, Pandas, NumPy, Matplotlib, Seaborn, Altair.
- **Interactive Apps**: Streamlit web dashboard.

---

## 📊 Running the Project Locally

### 1. Generate E-Commerce Clickstream & Basket Data
```bash
# Generate datasets
python scripts/generate_ecommerce_data.py

# Run conversion funnel analysis & generate Matplotlib plots
python scripts/funnel_analysis.py

# Run Market Basket Analysis & generate Seaborn affinity heatmap
python scripts/market_basket_analysis.py
```

### 2. Launch Interactive Web Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 👤 Author
**Kunisetty Giridhar Sai**  
- Email: [kunisettygiridharsai@gmail.com](mailto:kunisettygiridharsai@gmail.com)  
- LinkedIn: [linkedin.com/in/kunisetty-giridhar-sai](https://linkedin.com/in/kunisetty-giridhar-sai)  
- GitHub: [github.com/KUNISETTY-GIRIDHAR-SAI](https://github.com/KUNISETTY-GIRIDHAR-SAI)
