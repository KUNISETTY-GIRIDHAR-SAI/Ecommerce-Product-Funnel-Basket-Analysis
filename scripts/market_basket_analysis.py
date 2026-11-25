"""
Market Basket Analysis & Product Affinity Mining
Applies the Apriori association rule mining algorithm to order baskets,
calculates Support, Confidence, and Lift metrics, formulates cross-selling bundle
suggestions to improve Average Order Value (AOV), and generates visual affinity charts.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules

# Plot styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Segoe UI', 'font.size': 10})

script_dir = os.path.dirname(os.path.abspath(__file__))
items_path = os.path.join(script_dir, "..", "data", "order_items.csv")
orders_path = os.path.join(script_dir, "..", "data", "orders.csv")
vis_dir = os.path.join(script_dir, "..", "visualizations")
reports_dir = os.path.join(script_dir, "..", "reports")
os.makedirs(vis_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)

order_items = pd.read_csv(items_path)
orders = pd.read_csv(orders_path)

print(f"Loaded {len(order_items):,} order items across {len(orders):,} completed baskets.")

# 1. Create One-Hot Encoded Basket Matrix
basket = (order_items.groupby(["OrderID", "ProductName"])["Quantity"]
          .sum().unstack().reset_index().fillna(0)
          .set_index("OrderID"))

# Binarize quantities (>= 1 -> True, 0 -> False)
basket_encoded = basket.applymap(lambda x: True if x > 0 else False)

# 2. Run Apriori Algorithm (Support threshold = 1%)
frequent_itemsets = apriori(basket_encoded, min_support=0.015, use_colnames=True)
frequent_itemsets["length"] = frequent_itemsets["itemsets"].apply(lambda x: len(x))

# 3. Association Rules Generation (Confidence threshold >= 20%)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.1)
rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))

rules_sorted = rules.sort_values("lift", ascending=False).reset_index(drop=True)

print("\n--- TOP CO-PURCHASING AFFINITIES (ASSOCIATION RULES) ---")
display_cols = ["antecedents_str", "consequents_str", "support", "confidence", "lift"]
print(rules_sorted[display_cols].head(10).to_string(index=False))

# 4. Formulate Cross-Selling Bundle Recommendations
bundle_recommendations = []
seen_bundles = set()

for _, row in rules_sorted.iterrows():
    p1 = row["antecedents_str"]
    p2 = row["consequents_str"]
    bundle_pair = tuple(sorted([p1, p2]))
    if bundle_pair in seen_bundles:
        continue
    seen_bundles.add(bundle_pair)
    
    bundle_recommendations.append({
        "PrimaryProduct": p1,
        "RecommendedAddOn": p2,
        "Support": round(row["support"] * 100, 2),
        "ConfidencePct": round(row["confidence"] * 100, 1),
        "LiftScore": round(row["lift"], 2),
        "BundleType": "Frequently Bought Together (Cart Add-on)",
        "Strategy": f"Offer {p2} at 10% discount when {p1} is in cart"
    })

bundles_df = pd.DataFrame(bundle_recommendations).head(8)
bundles_df.to_csv(os.path.join(reports_dir, "bundle_cross_sell_recommendations.csv"), index=False)
print(f"\nSaved cross-selling bundle recommendations to {os.path.join(reports_dir, 'bundle_cross_sell_recommendations.csv')}")

# 5. Visualization 1: Top Bundles by Lift Score
fig, ax = plt.subplots(figsize=(10, 6))
top_bundles = bundles_df.sort_values("LiftScore", ascending=True)
y_labels = [f"{r['PrimaryProduct'][:22]}... + {r['RecommendedAddOn'][:22]}..." for _, r in top_bundles.iterrows()]
bars = ax.barh(range(len(top_bundles)), top_bundles["LiftScore"], color="#2563EB", height=0.6)
ax.set_yticks(range(len(top_bundles)))
ax.set_yticklabels(y_labels, fontsize=10, fontweight="600")
ax.set_xlabel("Affinity Lift Score (Multiplier above random chance)", fontsize=11, fontweight="bold")
ax.set_title("Top Co-Purchasing Bundles to Increase Average Order Value (AOV)", fontsize=13, fontweight="bold", pad=15)
ax.axvline(1.0, color="red", linestyle="--", alpha=0.7, label="Baseline (No affinity = 1.0)")

for bar, val in zip(bars, top_bundles["LiftScore"]):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f"{val:.2f}x Lift",
            va="center", fontweight="bold", fontsize=10, color="#1E3A8A")

ax.set_xlim(0, max(top_bundles["LiftScore"]) * 1.25)
ax.legend()
plt.tight_layout()
fig.savefig(os.path.join(vis_dir, "top_cross_sell_bundles.png"), dpi=300)
plt.close()

# 6. Visualization 2: Affinity Heatmap Matrix
top_products = order_items["ProductName"].value_counts().head(8).index
sub_basket = basket_encoded[top_products]
corr_matrix = sub_basket.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="Blues", cbar=True, ax=ax,
            linewidths=0.5, linecolor="#E2E8F0", annot_kws={"fontsize": 9, "fontweight": "bold"})
ax.set_title("Product Co-Purchasing Affinity Correlation Matrix", fontsize=14, fontweight="bold", pad=15)
ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right", fontsize=9)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)
plt.tight_layout()
fig.savefig(os.path.join(vis_dir, "market_basket_affinity_heatmap.png"), dpi=300)
plt.close()

print(f"Generated Market Basket affinity charts in {vis_dir}")
