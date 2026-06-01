# Task-4-ecommerce-data-visualization
Boardroom-ready data storytelling 7 charts + executive KPI dashboard built with matplotlib &amp; seaborn following the Architect-Editor-Storyteller framework
# 📈 ecommerce-data-visualization
> **DecodeLabs Industrial Training Kit — Project 4 (Mastery Phase)**  
> Batch 2026 | Data Analytics Track
## 📌 Project Overview

The final and optional mastery project in the DecodeLabs training track. This project is about **Data Storytelling** — translating complex numbers into clear, boardroom-ready visual insights that drive decisions.

Following the three pillars of professional data visualization:
| Pillar | Role | Principle |
|---|---|---|
| 1 | The Architect | Choose the right chart for the right question |
| 2 | The Editor | Eliminate chartjunk; maximize the data-ink ratio |
| 3 | The Storyteller | Write action titles that state the conclusion |

Every chart in this project answers a specific business question with a deliberate visual choice and an insight-driven title — not a descriptive one.
## 🎯 Objectives

- Select appropriate chart types based on the analytical need (comparison, trend, relationship, composition)
- Apply professional styling: zero-baseline axes, spotlight color, direct labels
- Write action titles that immediately communicate the business insight
- Build an executive KPI dashboard summarizing key metrics at a glance
- Deliver structured business recommendations using the SCR framework
## 🗂️ Dataset

| Property | Detail |
|---|---|
| File | `Project1_Cleaned_Dataset.xlsx` |
| Records | 1,200 orders |
| Columns | 15 |
| Date Range | January 2023 – June 2025 |
| Products | Monitor, Phone, Tablet, Chair, Printer, Laptop, Desk |
## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Core language |
| pandas | Data preparation and aggregation |
| matplotlib | All chart rendering |
| seaborn | Heatmap and statistical charts |
| numpy | Trend line computation |
| openpyxl | Dataset loading |
## 📁 Project Structure

ecommerce-data-visualization/
│
├── data/
│   └── Project1_Cleaned_Dataset.xlsx    # Input dataset
│
├── charts/                              # All generated chart outputs
│   ├── chart1_revenue_by_product.png
│   ├── chart2_monthly_revenue_trend.png
│   ├── chart3_status_payment_stacked.png
│   ├── chart4_referral_scatter.png
│   ├── chart5_coupon_boxplot.png
│   ├── chart6_product_yearly_grouped.png
│   ├── chart7_product_month_heatmap.png
│   └── dashboard_kpi_summary.png
│
├── Project4_Data_Visualization.py       # Main Python script
├── requirements.txt
└── README.md
## ▶️ How to Run

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ecommerce-data-visualization.git
cd ecommerce-data-visualization

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place dataset in same folder and run
python Project4_Data_Visualization.py
All 8 outputs will be saved automatically to the `charts/` folder.

## 📊 Charts & Business Questions

| Chart | Type | Business Question | Action Title |
|---|---|---|---|
| 1 | Horizontal Bar | Which product drives the most revenue? | Laptops & Monitors Lead Revenue — Together They Account for >40% of Sales |
| 2 | Line Chart | Is our monthly revenue growing? | Monthly Revenue Peaked in Mid-2024 but Shows Recovery Heading into 2025 |
| 3 | Stacked Bar | Which order status is costing us most? | Cancelled & Returned Orders Cost ~30% of Revenue |
| 4 | Scatter Plot | Which referral channel brings the highest-value customers? | Google & Email Referrals Generate Higher Revenue per Order Than Social |
| 5 | Box Plot | Do coupons increase revenue or just discount it? | Coupon Users Spend More on Average — SAVE10 Drives Highest Median Revenue |
| 6 | Grouped Bar | How do products perform year-over-year? | Laptop Revenue Grew YoY While Chair & Desk Sales Declined in 2025 |
| 7 | Heatmap | Are there seasonal patterns by product? | Monitors & Laptops Spike in Q4 — Align Inventory Before October |
| Dashboard | KPI Cards | What are our 7 most critical business metrics? | Executive Summary at a Glance |
## 💡 Key Insights (SCR Framework)

**Situation**  
The company processed 1,200 orders across Jan 2023 – Jun 2025, generating total revenue of $1,264,762 with an average order value of ~$1,054.

**Complication**  
Cancellations and returns account for ~41% of all orders — a significant revenue leak. Revenue dipped in Q3 2024, signaling a potential operational or demand issue.
**Resolution**
1. Double-down on Laptops — the highest and fastest-growing revenue product
2. Scale Google and Email acquisition — highest revenue per referred order
3. Investigate root causes of Cancelled/Returned orders; target below 10% loss rate
4. Pre-stock Monitors and Laptops before October to capture Q4 seasonal spikes
5. Expand coupon strategy — coupon users drive 74.5% of total revenue
## 🖼️ Sample Output

> All charts follow the 5-Second Rule: an executive must understand the core insight within five seconds of glancing at the chart.

- ✅ Zero-baseline axes on all bar charts
- ✅ Single accent color (Insight Blue) highlights the key data point
- ✅ Direct labels used instead of legends wherever possible
- ✅ Action titles state the conclusion, not the topic
- ✅ No 3D effects, no pie charts with more than 3 slices

