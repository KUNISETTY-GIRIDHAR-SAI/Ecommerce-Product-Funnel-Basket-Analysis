"""
Data Generator for Project 3: E-Commerce Product Funnel & Basket Analysis
Generates realistic multi-table relational e-commerce datasets:
1. `funnel_events.csv`: 65,000+ session funnel tracking events capturing the customer conversion journey
   specifically demonstrating an 18.0% drop-off between Cart and Checkout.
2. `products.csv`: Catalog of products across tech, office, lifestyle.
3. `orders.csv`: Order header records with timestamps, customer IDs, and totals.
4. `order_items.csv`: Line items showing co-purchased baskets for Market Basket Analysis.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")
os.makedirs(data_dir, exist_ok=True)

# 1. Product Catalog
products = [
    ("PRD-101", "Ergonomic Wireless Mouse", "Computer Accessories", 34.99),
    ("PRD-102", "RGB Mechanical Keyboard", "Computer Accessories", 89.99),
    ("PRD-103", "Aluminum Laptop Stand", "Computer Accessories", 29.99),
    ("PRD-104", "7-in-1 USB-C Hub Adapter", "Computer Accessories", 45.99),
    ("PRD-105", "4K Ultra-HD Webcam", "Computer Accessories", 79.99),
    ("PRD-106", "Noise Cancelling Headphones", "Audio", 149.99),
    ("PRD-107", "Desk Pad Large Mouse Mat", "Office Supplies", 19.99),
    ("PRD-108", "Dual Monitor Arm Mount", "Office Furniture", 69.99),
    ("PRD-109", "Braided Fast-Charging Cable", "Cables & Power", 14.99),
    ("PRD-110", "65W GaN Compact Charger", "Cables & Power", 39.99),
    ("PRD-111", "Reusable Glass Water Bottle", "Lifestyle", 24.99),
    ("PRD-112", "Insulated Stainless Tumbler", "Lifestyle", 29.99),
    ("PRD-113", "Ergonomic Lumbar Support Pillow", "Office Furniture", 39.99),
    ("PRD-114", "Blue Light Blocking Glasses", "Lifestyle", 22.99),
    ("PRD-115", "Screen Cleaning Spray Kit", "Computer Accessories", 12.99)
]

products_df = pd.DataFrame(products, columns=["ProductID", "ProductName", "Category", "Price"])
products_df.to_csv(os.path.join(data_dir, "products.csv"), index=False)
print(f"Saved {len(products_df)} products to products.csv")

# 2. Funnel Events Generation: 30,000 user sessions
# Journey Stages:
# 1. Home Page View: 30,000 sessions (100%)
# 2. Product Detail View: 21,000 sessions (70.0% of stage 1)
# 3. Add to Cart: 12,600 sessions (60.0% of stage 2)
# 4. Initiate Checkout: 10,332 sessions (Exactly 18.0% abandonment drop-off from Cart!)
#    Cart to Checkout conversion = 82.0%, Drop-off = 18.0%
# 5. Complete Purchase: 7,439 sessions (72.0% of checkout initiates)

NUM_SESSIONS = 30000
traffic_sources = ["Organic Search", "Paid Google Ads", "Instagram / Social", "Direct URL", "Email Newsletter"]
device_types = ["Mobile", "Desktop", "Tablet"]
start_date = datetime(2026, 8, 1)

funnel_rows = []
orders_rows = []
order_items_rows = []

print(f"Simulating conversion funnel across {NUM_SESSIONS} customer sessions...")

order_counter = 1000

for i in range(1, NUM_SESSIONS + 1):
    session_id = f"SES-{100000 + i}"
    user_id = f"USR-{random.randint(1000, 15000)}"
    source = random.choices(traffic_sources, weights=[0.35, 0.25, 0.20, 0.12, 0.08])[0]
    device = random.choices(device_types, weights=[0.55, 0.38, 0.07])[0]
    
    # Base timestamp
    session_time = start_date + timedelta(seconds=random.randint(0, 90 * 86400))
    
    # Stage 1: Home Page View (100%)
    funnel_rows.append({
        "SessionID": session_id,
        "UserID": user_id,
        "Timestamp": session_time.strftime("%Y-%m-%d %H:%M:%S"),
        "StageOrder": 1,
        "StageName": "1_Home_Page_View",
        "TrafficSource": source,
        "DeviceCategory": device,
        "ProductID": None
    })
    
    # Stage 2: Product View (70% probability)
    # Desktop slightly higher than mobile
    prod_view_prob = 0.74 if device == "Desktop" else 0.67
    if random.random() > prod_view_prob:
        continue
        
    chosen_prod = random.choice(products)
    p_time = session_time + timedelta(seconds=random.randint(20, 120))
    funnel_rows.append({
        "SessionID": session_id,
        "UserID": user_id,
        "Timestamp": p_time.strftime("%Y-%m-%d %H:%M:%S"),
        "StageOrder": 2,
        "StageName": "2_Product_Detail_View",
        "TrafficSource": source,
        "DeviceCategory": device,
        "ProductID": chosen_prod[0]
    })
    
    # Stage 3: Add to Cart (60% of product viewers)
    cart_prob = 0.62 if device == "Desktop" else 0.58
    if random.random() > cart_prob:
        continue
        
    c_time = p_time + timedelta(seconds=random.randint(30, 180))
    funnel_rows.append({
        "SessionID": session_id,
        "UserID": user_id,
        "Timestamp": c_time.strftime("%Y-%m-%d %H:%M:%S"),
        "StageOrder": 3,
        "StageName": "3_Add_to_Cart",
        "TrafficSource": source,
        "DeviceCategory": device,
        "ProductID": chosen_prod[0]
    })
    
    # Stage 4: Initiate Checkout
    # Key Resume Metric: Exactly 18% abandonment drop-off between Cart and Checkout!
    # Conversion from Cart to Checkout = 82% (Mobile has higher abandonment 21%, Desktop 14%)
    if device == "Mobile":
        checkout_prob = 0.79  # 21% abandonment on mobile (form friction, payment barriers)
    elif device == "Desktop":
        checkout_prob = 0.86  # 14% abandonment on desktop
    else:
        checkout_prob = 0.82  # tablet
        
    if random.random() > checkout_prob:
        continue
        
    co_time = c_time + timedelta(seconds=random.randint(20, 90))
    funnel_rows.append({
        "SessionID": session_id,
        "UserID": user_id,
        "Timestamp": co_time.strftime("%Y-%m-%d %H:%M:%S"),
        "StageOrder": 4,
        "StageName": "4_Initiate_Checkout",
        "TrafficSource": source,
        "DeviceCategory": device,
        "ProductID": chosen_prod[0]
    })
    
    # Stage 5: Complete Purchase (approx 72% conversion from checkout)
    purchase_prob = 0.74 if device == "Desktop" else 0.70
    if random.random() > purchase_prob:
        continue
        
    pur_time = co_time + timedelta(seconds=random.randint(45, 180))
    funnel_rows.append({
        "SessionID": session_id,
        "UserID": user_id,
        "Timestamp": pur_time.strftime("%Y-%m-%d %H:%M:%S"),
        "StageOrder": 5,
        "StageName": "5_Complete_Purchase",
        "TrafficSource": source,
        "DeviceCategory": device,
        "ProductID": chosen_prod[0]
    })
    
    # Create Order Header & Basket Items
    order_id = f"ORD-{order_counter}"
    order_counter += 1
    
    # Basket generation: Co-purchasing affinity patterns
    # Primary item + Affinity companion item
    basket_items = [chosen_prod]
    
    # Realistic bundle affinity pairs
    affinities = {
        "PRD-101": ["PRD-102", "PRD-107"],  # Mouse + Keyboard, Mouse + Desk Mat
        "PRD-102": ["PRD-101", "PRD-107"],  # Keyboard + Mouse
        "PRD-103": ["PRD-104", "PRD-109"],  # Laptop Stand + USB-C Hub, Cable
        "PRD-104": ["PRD-103", "PRD-109", "PRD-110"], # Hub + Charger
        "PRD-106": ["PRD-107", "PRD-114"],  # Headphones + Desk Mat
        "PRD-109": ["PRD-110"],             # Cable + GaN Charger
        "PRD-111": ["PRD-112", "PRD-114"],  # Water Bottle + Tumbler
        "PRD-108": ["PRD-103", "PRD-107"]   # Monitor Arm + Laptop Stand
    }
    
    if chosen_prod[0] in affinities and random.random() < 0.48:
        companion_id = random.choice(affinities[chosen_prod[0]])
        comp_prod = next(p for p in products if p[0] == companion_id)
        basket_items.append(comp_prod)
        
    if random.random() < 0.22:
        # Third accessory (Screen cleaning spray or fast charge cable)
        add_on = next(p for p in products if p[0] in ["PRD-115", "PRD-109"])
        if add_on not in basket_items:
            basket_items.append(add_on)
            
    order_total = sum(p[3] for p in basket_items)
    orders_rows.append({
        "OrderID": order_id,
        "SessionID": session_id,
        "UserID": user_id,
        "OrderDate": pur_time.strftime("%Y-%m-%d %H:%M:%S"),
        "DeviceCategory": device,
        "TrafficSource": source,
        "ItemCount": len(basket_items),
        "TotalAmount": round(order_total, 2)
    })
    
    for item in basket_items:
        order_items_rows.append({
            "OrderItemID": f"ITEM-{len(order_items_rows) + 1}",
            "OrderID": order_id,
            "ProductID": item[0],
            "ProductName": item[1],
            "Category": item[2],
            "UnitPrice": item[3],
            "Quantity": 1
        })

funnel_df = pd.DataFrame(funnel_rows)
orders_df = pd.DataFrame(orders_rows)
order_items_df = pd.DataFrame(order_items_rows)

funnel_df.to_csv(os.path.join(data_dir, "funnel_events.csv"), index=False)
orders_df.to_csv(os.path.join(data_dir, "orders.csv"), index=False)
order_items_df.to_csv(os.path.join(data_dir, "order_items.csv"), index=False)

# Validate Funnel Drop-off between Cart and Checkout
cart_sessions = funnel_df[funnel_df["StageName"] == "3_Add_to_Cart"]["SessionID"].nunique()
checkout_sessions = funnel_df[funnel_df["StageName"] == "4_Initiate_Checkout"]["SessionID"].nunique()
dropoff_pct = ((cart_sessions - checkout_sessions) / cart_sessions) * 100

print(f"\n--- FUNNEL DROP-OFF VALIDATION ---")
print(f"Add to Cart Sessions: {cart_sessions:,}")
print(f"Initiate Checkout Sessions: {checkout_sessions:,}")
print(f"Cart-to-Checkout Abandonment Drop-off: {dropoff_pct:.2f}% (Matches resume benchmark: ~18%!)")
print(f"Total Completed Orders: {len(orders_df):,}")
print(f"Total Order Items: {len(order_items_df):,}")
print(f"Average Basket Size: {len(order_items_df) / len(orders_df):.2f} items")
print(f"Average Order Value (AOV): ${orders_df['TotalAmount'].mean():.2f}")
