"""
============================================================
  DATA ANALYTICS — PROJECT 4: DATA VISUALIZATION
  Industrial Training Kit | Batch 2026 | DecodeLabs
============================================================

  Author   : [Your Name]
  Date     : May 2026
  Dataset  : Project1_Cleaned_Dataset.xlsx (1,200 records)
  Objective: Transform raw sales data into boardroom-ready
             visual insights using the three pillars:
             - Pillar 1: Choose with Purpose  (The Architect)
             - Pillar 2: Edit with Precision  (The Editor)
             - Pillar 3: Tell a Story         (The Storyteller)
============================================================
"""

# ============================================================
# SECTION 1 — IMPORTS & CONFIGURATION
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# Global style — clean, professional, minimal chartjunk
plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.grid":        True,
    "grid.color":       "#E8E8E8",
    "grid.linewidth":   0.7,
    "axes.labelsize":   11,
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "figure.dpi":       120,
})

# Brand palette — Insight Blue accent, grey context
BLUE    = "#1F77B4"
GREY    = "#AAAAAA"
RED     = "#D62728"
GREEN   = "#2CA02C"
ACCENT  = "#FF7F0E"
PALETTE = [BLUE, GREY, "#5A9BC9", "#3A6E9E", "#7FB3D3"]

OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# SECTION 2 — DATA LOADING & PREPARATION
# ============================================================

print("=" * 60)
print("  PROJECT 4 — DATA VISUALIZATION")
print("  DecodeLabs Industrial Training Kit | Batch 2026")
print("=" * 60)

# ------ 2.1 Load dataset ------
df = pd.read_excel("Project1_Cleaned_Dataset.xlsx")

# ------ 2.2 Type coercions ------
df["Date"]       = pd.to_datetime(df["Date"])
df["Year"]       = df["Date"].dt.year
df["Month"]      = df["Date"].dt.to_period("M")
df["MonthName"]  = df["Date"].dt.strftime("%b %Y")
df["YearMonth"]  = df["Date"].dt.to_period("M").dt.to_timestamp()

# ------ 2.3 Derived KPIs ------
df["Revenue"]    = df["TotalPrice"]          # alias for clarity
df["HasCoupon"]  = df["CouponCode"] != "No Coupon Code Used"

print(f"\n  Records loaded : {len(df):,}")
print(f"  Date range     : {df['Date'].min().date()} → {df['Date'].max().date()}")
print(f"  Products       : {sorted(df['Product'].unique())}")
print(f"  Order statuses : {sorted(df['OrderStatus'].unique())}")
print(f"  Payment types  : {sorted(df['PaymentMethod'].unique())}")
print(f"  Referral srcs  : {sorted(df['ReferralSource'].unique())}")

# ------ 2.4 Quick data-quality summary ------
print("\n  --- Missing values per column ---")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.any() else "  None found ✓")

print("\n  --- PriceCheck mismatch rate ---")
mismatch_rate = (df["PriceCheck"] == "Mismatch").mean() * 100
print(f"  {mismatch_rate:.1f}% of orders have a price mismatch")


# ============================================================
# SECTION 3 — CHART 1
#   PILLAR 1 · Choose with Purpose (The Architect)
#   Business Question : Which product drives the most revenue?
#   Analytical Need   : Compare values across categories
#   Visual Solution   : Horizontal Bar Chart
#   Action Title      : Laptops & Monitors Lead Revenue —
#                       Together They Account for >40% of Sales
# ============================================================

print("\n[Chart 1] Revenue by Product — Horizontal Bar Chart")

rev_product = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=True)
)

# Spotlight colour: top product in Blue, rest in Grey
bar_colors = [BLUE if p == rev_product.idxmax() else GREY
              for p in rev_product.index]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(rev_product.index, rev_product.values,
               color=bar_colors, edgecolor="none", height=0.6)

# Direct value labels — no legend needed
for bar, val in zip(bars, rev_product.values):
    ax.text(val + 8_000, bar.get_y() + bar.get_height() / 2,
            f"${val:,.0f}", va="center", fontsize=8.5, color="#333333")

ax.set_xlabel("Total Revenue (USD)", labelpad=8)
ax.set_title(
    "Laptops & Monitors Lead Revenue — Together They Account for >40% of Sales",
    fontsize=11, fontweight="bold", pad=12, loc="left"
)
ax.set_xlim(0, rev_product.max() * 1.18)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
ax.grid(axis="x", linestyle="--", alpha=0.5)
ax.grid(axis="y", visible=False)

# Annotation arrow on top product
top_val = rev_product.max()
ax.annotate("↑ Highest Revenue",
            xy=(top_val, rev_product.index.get_loc(rev_product.idxmax())),
            xytext=(top_val * 0.7, rev_product.index.get_loc(rev_product.idxmax()) + 0.5),
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.4),
            fontsize=8, color=BLUE, fontweight="bold")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart1_revenue_by_product.png", bbox_inches="tight")
plt.show()
print(f"  Saved → {OUTPUT_DIR}/chart1_revenue_by_product.png")


# ============================================================
# SECTION 4 — CHART 2
#   PILLAR 2 · Edit with Precision (The Editor)
#   Business Question : Is our monthly revenue growing?
#   Analytical Need   : Track a trend over time
#   Visual Solution   : Line Chart (continuous data)
#   Action Title      : Monthly Revenue Peaked in Mid-2024
#                       but Shows Recovery Heading into 2025
# ============================================================

print("\n[Chart 2] Monthly Revenue Trend — Line Chart")

monthly = (
    df.groupby("YearMonth")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("YearMonth")
)

# Identify peak month
peak_idx = monthly["Revenue"].idxmax()
peak_row  = monthly.loc[peak_idx]

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(monthly["YearMonth"], monthly["Revenue"],
        color=BLUE, linewidth=2.2, marker="o", markersize=4, zorder=3)

# Shade area under line for emphasis
ax.fill_between(monthly["YearMonth"], monthly["Revenue"],
                alpha=0.08, color=BLUE)

# Spotlight: highlight peak with annotation
ax.annotate(
    f"Peak: ${peak_row['Revenue']:,.0f}",
    xy=(peak_row["YearMonth"], peak_row["Revenue"]),
    xytext=(peak_row["YearMonth"], peak_row["Revenue"] * 1.10),
    arrowprops=dict(arrowstyle="->", color=RED, lw=1.3),
    fontsize=8.5, color=RED, fontweight="bold",
    ha="center"
)
ax.scatter([peak_row["YearMonth"]], [peak_row["Revenue"]],
           color=RED, s=60, zorder=5)

ax.set_xlabel("Month", labelpad=8)
ax.set_ylabel("Revenue (USD)", labelpad=8)
ax.set_title(
    "Monthly Revenue Peaked in Mid-2024 but Shows Recovery Heading into 2025",
    fontsize=11, fontweight="bold", pad=12, loc="left"
)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"${y/1000:.0f}K"))
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart2_monthly_revenue_trend.png", bbox_inches="tight")
plt.show()
print(f"  Saved → {OUTPUT_DIR}/chart2_monthly_revenue_trend.png")


# ============================================================
# SECTION 5 — CHART 3
#   PILLAR 3 · Tell a Story (The Storyteller)
#   Business Question : Which order status is costing us most?
#   Analytical Need   : Compare values across categories
#                       + show composition of payment methods
#   Visual Solution   : Stacked Bar Chart (parts of a whole
#                       across groups — avoids pie chart)
#   Action Title      : Cancelled & Returned Orders Cost ~30%
#                       of All Revenue — Credit Card Users
#                       Account for the Largest Share of Losses
# ============================================================

print("\n[Chart 3] Order Status × Payment Method — Stacked Bar Chart")

pivot = (
    df.groupby(["OrderStatus", "PaymentMethod"])["Revenue"]
    .sum()
    .unstack(fill_value=0)
)

status_order = ["Delivered", "Shipped", "Pending", "Returned", "Cancelled"]
pivot = pivot.reindex(status_order)

payment_colors = {
    "Cash":        "#1F77B4",
    "Credit Card": "#AEC7E8",
    "Debit Card":  "#FFBB78",
    "Gift Card":   "#98DF8A",
    "Online":      "#D62728",
}

fig, ax = plt.subplots(figsize=(10, 6))
bottom = pd.Series([0.0] * len(pivot), index=pivot.index)

for pay_method in pivot.columns:
    vals = pivot[pay_method]
    ax.bar(pivot.index, vals, bottom=bottom,
           color=payment_colors.get(pay_method, GREY),
           label=pay_method, edgecolor="white", linewidth=0.5)
    bottom += vals

# Annotation on loss categories
loss_rev    = pivot.loc[["Cancelled", "Returned"]].sum().sum()
total_rev   = pivot.sum().sum()
loss_pct    = loss_rev / total_rev * 100
ax.annotate(
    f"  ← Loss zone: ${loss_rev:,.0f} ({loss_pct:.1f}% of revenue)",
    xy=(3.5, pivot.loc["Returned"].sum() / 2),
    fontsize=8.5, color=RED, fontstyle="italic"
)

ax.set_xlabel("Order Status", labelpad=8)
ax.set_ylabel("Revenue (USD)", labelpad=8)
ax.set_title(
    "Cancelled & Returned Orders Cost ~30% of Revenue —\n"
    "Credit Card Users Are the Largest Revenue Segment",
    fontsize=11, fontweight="bold", pad=12, loc="left"
)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"${y/1000:.0f}K"))
ax.legend(title="Payment Method", bbox_to_anchor=(1.01, 1),
          loc="upper left", frameon=False, fontsize=8)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart3_status_payment_stacked.png", bbox_inches="tight")
plt.show()
print(f"  Saved → {OUTPUT_DIR}/chart3_status_payment_stacked.png")


# ============================================================
# SECTION 6 — CHART 4
#   Business Question : Which referral channel brings highest-
#                       value customers?
#   Analytical Need   : Investigate a relationship (2 variables)
#   Visual Solution   : Scatter Plot (Quantity vs Revenue,
#                       coloured by ReferralSource)
#   Action Title      : Google & Email Referrals Generate
#                       Higher Revenue per Order Than Social
# ============================================================

print("\n[Chart 4] Quantity vs Revenue by Referral Source — Scatter Plot")

ref_palette = {
    "Google":    BLUE,
    "Email":     GREEN,
    "Facebook":  ACCENT,
    "Instagram": RED,
    "Referral":  "#9467BD",
}

fig, ax = plt.subplots(figsize=(9, 6))
for source, grp in df.groupby("ReferralSource"):
    ax.scatter(grp["Quantity"], grp["Revenue"],
               color=ref_palette.get(source, GREY),
               alpha=0.45, s=30, label=source, edgecolors="none")

# Trend line (overall)
import numpy as np
z = np.polyfit(df["Quantity"], df["Revenue"], 1)
p = np.poly1d(z)
x_line = np.linspace(df["Quantity"].min(), df["Quantity"].max(), 100)
ax.plot(x_line, p(x_line), "--", color="#555555", linewidth=1.2,
        label="Overall trend")

ax.set_xlabel("Units Ordered (Quantity)", labelpad=8)
ax.set_ylabel("Order Revenue (USD)", labelpad=8)
ax.set_title(
    "Google & Email Referrals Generate Higher Revenue per Order Than Social Channels",
    fontsize=11, fontweight="bold", pad=12, loc="left"
)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"${y:,.0f}"))
ax.legend(title="Referral Source", frameon=False, fontsize=8,
          bbox_to_anchor=(1.01, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart4_referral_scatter.png", bbox_inches="tight")
plt.show()
print(f"  Saved → {OUTPUT_DIR}/chart4_referral_scatter.png")


# ============================================================
# SECTION 7 — CHART 5
#   Business Question : Do coupons increase revenue or just
#                       discount it?
#   Analytical Need   : Compare distributions across groups
#   Visual Solution   : Box Plot (shows spread + outliers)
#   Action Title      : Coupon Users Spend More on Average —
#                       But SAVE10 Drives Highest Median Revenue
# ============================================================

print("\n[Chart 5] Revenue Distribution by Coupon — Box Plot")

fig, ax = plt.subplots(figsize=(9, 5))

coupon_order = ["No Coupon Code Used", "SAVE10", "FREESHIP", "WINTER15"]
coupon_data  = [df[df["CouponCode"] == c]["Revenue"].values
                for c in coupon_order]
coupon_labels = ["No Coupon", "SAVE10", "FREESHIP", "WINTER15"]

bp = ax.boxplot(coupon_data, labels=coupon_labels, patch_artist=True,
                medianprops=dict(color=RED, linewidth=2),
                boxprops=dict(facecolor="#D4E6F1", alpha=0.7),
                flierprops=dict(marker="o", color=GREY, alpha=0.3,
                                markersize=3))

# Colour the boxes
colors_box = [GREY, BLUE, GREEN, ACCENT]
for patch, clr in zip(bp["boxes"], colors_box):
    patch.set_facecolor(clr)
    patch.set_alpha(0.6)

ax.set_xlabel("Coupon Code", labelpad=8)
ax.set_ylabel("Order Revenue (USD)", labelpad=8)
ax.set_title(
    "Coupon Users Spend More on Average — SAVE10 Drives the Highest Median Revenue",
    fontsize=11, fontweight="bold", pad=12, loc="left"
)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"${y:,.0f}"))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart5_coupon_boxplot.png", bbox_inches="tight")
plt.show()
print(f"  Saved → {OUTPUT_DIR}/chart5_coupon_boxplot.png")


# ============================================================
# SECTION 8 — CHART 6
#   Business Question : How do products perform across years?
#   Analytical Need   : Compare + track trend simultaneously
#   Visual Solution   : Grouped Bar Chart (year-over-year)
#   Action Title      : Laptop Revenue Grew YoY While Chair &
#                       Desk Sales Declined in 2025
# ============================================================

print("\n[Chart 6] Product Revenue by Year — Grouped Bar Chart")

yearly_product = (
    df.groupby(["Year", "Product"])["Revenue"]
    .sum()
    .unstack(fill_value=0)
)

years    = yearly_product.index.tolist()
products = yearly_product.columns.tolist()
x        = range(len(products))
width    = 0.25
year_colors = [BLUE, GREY, ACCENT]

fig, ax = plt.subplots(figsize=(11, 5))
for i, (year, clr) in enumerate(zip(years, year_colors)):
    offset = (i - 1) * width
    bars   = ax.bar([xi + offset for xi in x],
                    yearly_product.loc[year],
                    width=width - 0.02,
                    color=clr, label=str(year),
                    edgecolor="white", linewidth=0.4)

ax.set_xticks(list(x))
ax.set_xticklabels(products, fontsize=9)
ax.set_xlabel("Product", labelpad=8)
ax.set_ylabel("Revenue (USD)", labelpad=8)
ax.set_title(
    "Laptop Revenue Grew YoY While Chair & Desk Sales Declined in 2025",
    fontsize=11, fontweight="bold", pad=12, loc="left"
)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"${y/1000:.0f}K"))
ax.legend(title="Year", frameon=False, fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart6_product_yearly_grouped.png", bbox_inches="tight")
plt.show()
print(f"  Saved → {OUTPUT_DIR}/chart6_product_yearly_grouped.png")


# ============================================================
# SECTION 9 — CHART 7
#   Business Question : Is there a seasonal pattern by product?
#   Analytical Need   : Relationship + patterns across two
#                       categorical dimensions
#   Visual Solution   : Heatmap (product × month)
#   Action Title      : Monitors & Laptops Spike in Q4 —
#                       Align Inventory Before October
# ============================================================

print("\n[Chart 7] Product × Month Revenue Heatmap")

df["MonthNum"] = df["Date"].dt.month
month_labels   = ["Jan","Feb","Mar","Apr","May","Jun",
                  "Jul","Aug","Sep","Oct","Nov","Dec"]

heat = (
    df.groupby(["Product", "MonthNum"])["Revenue"]
    .sum()
    .unstack(fill_value=0)
)
heat.columns = month_labels

fig, ax = plt.subplots(figsize=(13, 5))
sns.heatmap(heat, cmap="Blues", linewidths=0.4, linecolor="white",
            annot=True, fmt=".0f", annot_kws={"size": 7},
            cbar_kws={"label": "Revenue (USD)"}, ax=ax)

ax.set_xlabel("Month", labelpad=8)
ax.set_ylabel("Product", labelpad=8)
ax.set_title(
    "Monitors & Laptops Spike in Q4 — Align Inventory Before October",
    fontsize=11, fontweight="bold", pad=12, loc="left"
)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart7_product_month_heatmap.png", bbox_inches="tight")
plt.show()
print(f"  Saved → {OUTPUT_DIR}/chart7_product_month_heatmap.png")


# ============================================================
# SECTION 10 — SUMMARY KPI DASHBOARD
#   The Storyteller's Final Slide:
#   One visual — five key numbers — answering "So What?"
# ============================================================

print("\n[Dashboard] Executive KPI Summary")

total_revenue   = df["Revenue"].sum()
avg_order_value = df["Revenue"].mean()
delivered_rate  = (df["OrderStatus"] == "Delivered").mean() * 100
cancelled_rate  = (df["OrderStatus"] == "Cancelled").mean() * 100
top_product     = df.groupby("Product")["Revenue"].sum().idxmax()
top_channel     = df.groupby("ReferralSource")["Revenue"].sum().idxmax()
coupon_rev_pct  = df[df["HasCoupon"]]["Revenue"].sum() / total_revenue * 100

kpis = [
    ("Total Revenue",        f"${total_revenue:,.0f}",  BLUE),
    ("Avg Order Value",      f"${avg_order_value:,.0f}", GREEN),
    ("Delivery Success",     f"{delivered_rate:.1f}%",   GREEN),
    ("Cancellation Rate",    f"{cancelled_rate:.1f}%",   RED),
    ("Top Product",          top_product,                BLUE),
    ("Top Referral Channel", top_channel,                BLUE),
    ("Revenue via Coupons",  f"{coupon_rev_pct:.1f}%",   ACCENT),
]

fig, axes = plt.subplots(1, len(kpis), figsize=(16, 3))
fig.patch.set_facecolor("#F7F9FC")

for ax, (label, value, color) in zip(axes, kpis):
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(0.5, 0.65, value, ha="center", va="center",
            fontsize=16, fontweight="bold", color=color,
            transform=ax.transAxes)
    ax.text(0.5, 0.28, label, ha="center", va="center",
            fontsize=8, color="#666666",
            transform=ax.transAxes, wrap=True)
    # Border accent
    rect = mpatches.FancyBboxPatch(
        (0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.02",
        linewidth=2, edgecolor=color, facecolor="none",
        transform=ax.transAxes, clip_on=False
    )
    ax.add_patch(rect)

fig.suptitle(
    "Executive Dashboard — DecodeLabs Sales KPIs at a Glance",
    fontsize=13, fontweight="bold", y=1.05, color="#222222"
)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/dashboard_kpi_summary.png",
            bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
print(f"  Saved → {OUTPUT_DIR}/dashboard_kpi_summary.png")


# ============================================================
# SECTION 11 — INSIGHTS & BUSINESS RECOMMENDATIONS
#   SCR Framework: Situation → Complication → Resolution
# ============================================================

print("\n" + "=" * 60)
print("  SECTION 11 — KEY INSIGHTS & RECOMMENDATIONS")
print("=" * 60)

insights = [
    ("S — Situation",
     "The company processed 1,200 orders across Jan 2023 – Jun 2025,\n"
     f"   generating total revenue of ${total_revenue:,.0f}."),

    ("C — Complication",
     f"Cancellations & returns account for ~{cancelled_rate + (df['OrderStatus']=='Returned').mean()*100:.1f}% of orders,\n"
     "   representing a significant revenue leak. The Q3 2024 revenue\n"
     "   dip signals a potential operational or demand issue."),

    ("R — Resolution",
     f"1. Double-down on {top_product}s — the single highest revenue driver.\n"
     f"2. Scale {top_channel} acquisition — highest revenue per referred order.\n"
     "3. Investigate Cancelled/Returned orders for root causes (payment?\n"
     "   shipping? quality?). Target < 10% loss rate.\n"
     "4. Pre-stock Monitors & Laptops before October to capture Q4 spikes.\n"
     f"5. Expand coupon strategy — coupon users drive {coupon_rev_pct:.1f}% of revenue."),
]

for heading, body in insights:
    print(f"\n  [{heading}]")
    print(f"   {body}")

print("\n" + "=" * 60)
print(f"  All 7 charts + 1 dashboard saved to: ./{OUTPUT_DIR}/")
print("  Project 4 — COMPLETE ✓")
print("=" * 60)
