# 📊 Vendor Performance and Profitability Analysis | Data Analytics Project

**🛠 Tools & Technologies:** Python (Pandas, SQLAlchemy, Matplotlib), Microsoft SQL Server, Power BI, Logging, Data Cleaning & EDA

## 🚀 Project Overview
Designed and implemented a complete data analytics pipeline to analyze **vendor performance, profitability, and inventory efficiency** for a retail inventory system. The workflow included automated data ingestion, cleaning, transformation, and visualization through an interactive dashboard.  

## ✨ Key Contributions

### ⚡ Automated Data Ingestion
- Developed a Python script using `pandas`, `SQLAlchemy`, and `pyodbc` to ingest multiple CSV files into an SQL Server database.
- Implemented **robust logging** and error handling for seamless automation.  

### 🧹 Data Cleaning & Transformation
- Created a **vendor summary table** by joining multiple relational tables (`purchases`, `sales`, `vendor_invoice`, `purchase_prices`) via complex SQL CTE queries.
- Cleaned and standardized numeric and categorical fields.
- Engineered key performance metrics: **Gross Profit 💰**, **Profit Margin 📈**, **Stock Turnover 🔄**, **Sales-to-Purchase Ratio 📊**.

### 🔎 Exploratory Data Analysis (EDA)
- Identified **loss-making vendors ❌** and inventory inefficiencies through negative and zero-value analysis.
- Found strong positive correlation (0.999) between purchase and sales quantities ✅, validating efficient inventory flow.
- Discovered weak correlation between price and profit 💸, indicating pricing independence from sales outcomes.
- Detected outliers in **freight cost 🚚** and purchase prices, highlighting potential logistics optimization opportunities.

### 📊 Statistical Analysis
- Conducted **hypothesis testing** to validate significant differences in profit margins between top- and low-performing vendors.
- Revealed that **top vendors dominate 65% of total purchases ⚠️**, suggesting supplier dependency risks.

### 💡 Data-Driven Insights
- Large-order vendors benefit from ~72% lower unit costs 💵, supporting bulk purchase strategies.
- Identified **$2.71M in unsold inventory 🏷**, recommending improved stock management.
- Suggested **targeted promotions 🎯** for high-margin, low-sales brands and vendor diversification to enhance resilience.

### 📈 Dashboard Development
- Designed a **Power BI dashboard** visualizing vendor performance KPIs, sales vs. purchase trends, inventory turnover, and profitability distribution for strategic decision-making.

## 🌟 Impact
Enabled management to make **data-driven pricing, purchasing, and marketing decisions**—optimizing vendor relationships and improving profitability through actionable insights.
