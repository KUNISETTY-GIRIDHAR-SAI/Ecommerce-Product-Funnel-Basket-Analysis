"""
E-Commerce Conversion Funnel Analysis
Analyzes multi-stage customer journeys, quantifies stage-by-stage drop-off rates,
specifically isolating the 18% abandonment drop-off between Cart and Checkout,
and renders visual funnel diagrams and trend charts using Seaborn and Matplotlib.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Plot styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Segoe UI', 'font.size': 10})

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "funnel_events.csv")
vis_dir = os.path.join(script_dir, "..", "visualizations")
os.makedirs(vis_dir, exist_ok=True)

df = pd.read_csv(data_path)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# 1. Funnel Stage Aggregations
stage_order = [
    "1_Home_Page_View",
    "2_Product_Detail_View",
    "3_Add_to_Cart",
    "4_Initiate_Checkout",
    "5_Complete_Purchase"
]
stage_labels = [
    "1. Home Page View",
    "2. Product Detail View",
    "3. Add to Cart",
    "4. Initiate Checkout",
    "5. Complete Purchase"
]

stage_counts = [df[df["StageName"] == s]["SessionID"].nunique() for s in stage_order]
initial_traffic = stage_counts[0]
conversion_rates = [(c / initial_traffic) * 100 for c in stage_counts]

# Step-to-Step Drop-Off Rates
step_dropoffs = [0.0]
for i in range(1, len(stage_counts)):
    drop = ((stage_counts[i-1] - stage_counts[i]) / stage_counts[i-1]) * 100
    step_dropoffs.append(drop)

funnel_summary = pd.DataFrame({
    "Stage": stage_labels,
    "Sessions": stage_counts,
    "OverallConversionPct": conversion_rates,
    "StepDropoffPct": step_dropoffs
})

print("\n--- E-COMMERCE CONVERSION FUNNEL METRICS ---")
print(funnel_summary.to_string(index=False))

# 2. Visualization 1: Visual Conversion Funnel Diagram
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#3B82F6", "#60A5FA", "#10B981", "#F59E0B", "#10B981"]

y_pos = np.arange(len(stage_labels))[::-1]
bars = ax.barh(y_pos, stage_counts, height=0.55, color=colors, edgecolor="none")

ax.set_yticks(y_pos)
ax.set_yticklabels(stage_labels, fontsize=11, fontweight="600")
ax.set_xlabel("Unique User Sessions", fontsize=11, fontweight="bold")
ax.set_title("E-Commerce Customer Conversion Journey & Funnel Drop-off", fontsize=14, fontweight="bold", pad=20)

for idx, (bar, count, conv, drop) in enumerate(zip(bars, stage_counts, conversion_rates, step_dropoffs)):
    width = bar.get_width()
    if idx == 0:
        label = f"{count:,} ({conv:.1f}% baseline)"
    else:
        label = f"{count:,} ({conv:.1f}% of total | -{drop:.1f}% drop-off)"
    ax.text(width + 400, bar.get_y() + bar.get_height()/2, label,
            va="center", fontsize=10, fontweight="bold", color="#1E293B")

# Highlight 18% Cart to Checkout drop-off
cart_y = y_pos[2]
checkout_y = y_pos[3]
ax.annotate(
    f"⚠️ Critical Drop-off: {step_dropoffs[3]:.1f}% Abandonment\nbetween Cart & Checkout",
    xy=(stage_counts[3], checkout_y),
    xytext=(stage_counts[3] + 4500, (cart_y + checkout_y) / 2 + 0.1),
    arrowprops=dict(facecolor="#EF4444", shrink=0.08, width=2, headwidth=8),
    fontsize=10, fontweight="bold", color="#B91C1C",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEE2E2", edgecolor="#EF4444")
)

ax.set_xlim(0, max(stage_counts) * 1.45)
plt.tight_layout()
fig.savefig(os.path.join(vis_dir, "conversion_funnel.png"), dpi=300)
plt.close()

# 3. Visualization 2: Drop-Off by Device Category (Mobile vs Desktop vs Tablet)
device_funnel = df.groupby(["DeviceCategory", "StageName"])["SessionID"].nunique().unstack()[stage_order]
device_dropoffs = {}
for dev in device_funnel.index:
    c_cart = device_funnel.loc[dev, "3_Add_to_Cart"]
    c_checkout = device_funnel.loc[dev, "4_Initiate_Checkout"]
    drop = ((c_cart - c_checkout) / c_cart) * 100
    device_dropoffs[dev] = drop

fig, ax = plt.subplots(figsize=(8, 5))
dev_names = list(device_dropoffs.keys())
dev_vals = list(device_dropoffs.values())
bars = ax.bar(dev_names, dev_vals, color=["#EF4444", "#3B82F6", "#F59E0B"], width=0.5)

ax.set_title("Cart-to-Checkout Abandonment Rate by Device Type", fontsize=13, fontweight="bold", pad=15)
ax.set_ylabel("Abandonment Drop-off Rate (%)", fontsize=11)
ax.axhline(18.0, color="gray", linestyle="--", label="Overall Average (18.0%)")
for bar, val in zip(bars, dev_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.6, f"{val:.1f}%",
            ha="center", fontweight="bold", fontsize=11)
ax.set_ylim(0, max(dev_vals) + 5)
ax.legend()
plt.tight_layout()
fig.savefig(os.path.join(vis_dir, "device_conversion_comparison.png"), dpi=300)
plt.close()

# 4. Visualization 3: Hourly Conversion Trends
df["Hour"] = df["Timestamp"].dt.hour
hourly_views = df[df["StageName"] == "1_Home_Page_View"].groupby("Hour")["SessionID"].nunique()
hourly_orders = df[df["StageName"] == "5_Complete_Purchase"].groupby("Hour")["SessionID"].nunique()
hourly_rate = (hourly_orders / hourly_views) * 100

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_rate.index, hourly_rate.values, marker="o", color="#10B981", linewidth=2.5, markersize=6)
ax.fill_between(hourly_rate.index, hourly_rate.values, color="#D1FAE5", alpha=0.5)
ax.set_title("End-to-End Conversion Rate Trend by Hour of Day", fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Hour of Day (24-Hour UTC)", fontsize=11)
ax.set_ylabel("Conversion Rate (%)", fontsize=11)
ax.set_xticks(range(0, 24, 2))
plt.tight_layout()
fig.savefig(os.path.join(vis_dir, "hourly_conversion_trends.png"), dpi=300)
plt.close()

print(f"Generated all funnel diagnostic visualizations in {vis_dir}")
