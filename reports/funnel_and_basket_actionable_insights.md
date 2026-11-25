# E-Commerce Product Funnel & Basket Analysis Report

**Author**: Kunisetty Giridhar Sai  
**Dataset Scope**: 30,000 User Sessions, 65,000+ Clickstream Funnel Events, 7,400+ Completed Orders  
**Tech Stack**: Python (Pandas, Matplotlib, Seaborn, Mlxtend) · MySQL  

---

## 1. Executive Summary
Through multi-table MySQL joins and exploratory clickstream funnel analysis across **30,000 customer sessions**, we mapped the end-to-end customer conversion journey:
`Home Page View` -> `Product Detail View` -> `Add to Cart` -> `Initiate Checkout` -> `Complete Purchase`.

Crucially, the analysis identified a sharp **18.0% abandonment drop-off between Cart and Checkout** (2,268 potential buyers abandoning filled carts before initiating checkout).

To recover this lost revenue and elevate basket sizes, we executed **Market Basket Analysis (Apriori association rule mining)** on completed orders, uncovering strong affinity pairs (e.g., Wireless Mouse + Mechanical Keyboard with **2.84x Lift**; Laptop Stand + 7-in-1 USB-C Hub with **3.12x Lift**). Deploying these dynamic bundles at the cart stage provides a direct path to both recovering cart drop-off and increasing Average Order Value (AOV) by an estimated **14.5%**.

---

## 2. Customer Conversion Journey & Funnel Drop-Off

| Funnel Stage | Unique Sessions | Retention from Top (%) | Stage-to-Stage Drop-Off (%) | Operational Diagnosis |
| :--- | :---: | :---: | :---: | :--- |
| **1. Home Page View** | 30,000 | 100.0% | 0.0% | Top of funnel baseline |
| **2. Product Detail View** | 21,048 | 70.2% | -29.8% | Healthy catalog engagement |
| **3. Add to Cart** | 12,612 | 42.0% | -40.1% | Strong purchase intent |
| **4. Initiate Checkout** | **10,344** | **34.5%** | **-18.0%** | **⚠️ Critical Abandonment Drop-off** |
| **5. Complete Purchase** | 7,452 | 24.8% | -27.9% | Final order completion |

### Deep-Dive: Root Causes of the 18% Cart-to-Checkout Abandonment
Segmentation by device category pinpointed the primary friction points:
1. **Mobile Abandonment (21.2%) vs Desktop (14.1%)**:
   - Mobile users faced higher checkout friction: lack of native 1-click payment options (Apple Pay, Google Pay).
   - Surprise shipping fees revealed only after cart entry.
   - Forced account registration requirement prior to checkout initiation.

---

## 3. Market Basket Analysis & Top Co-Purchasing Affinities

Applying the Apriori algorithm with support threshold $\ge 1.5\%$ and confidence $\ge 20\%$ identified the following top cross-selling affinities:

| Primary Item (Antecedent) | Recommended Add-On (Consequent) | Support (%) | Confidence (%) | Lift Score | Recommended Strategic Bundle |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Aluminum Laptop Stand** | **7-in-1 USB-C Hub Adapter** | 3.2% | 46.8% | **3.12x** | *"Ergonomic Workstation Pro Bundle"* (10% off Hub) |
| **Ergonomic Wireless Mouse** | **RGB Mechanical Keyboard** | 4.1% | 51.2% | **2.84x** | *"Master Desk Setup"* (Free mousepad included) |
| **Braided Fast-Charging Cable** | **65W GaN Compact Charger** | 2.8% | 42.5% | **2.65x** | *"Power Duo Fast-Charge Pack"* |
| **Dual Monitor Arm Mount** | **Aluminum Laptop Stand** | 2.1% | 38.4% | **2.41x** | *"Dual Screen Ergonomics Kit"* |
| **Noise Cancelling Headphones** | **Desk Pad Large Mouse Mat** | 2.4% | 33.1% | **2.15x** | *"Focus & Audio Comfort Bundle"* |

---

## 4. Actionable Recommendations to Improve Conversion & AOV

1. **Resolve Cart-to-Checkout Friction**:
   - Implement **Guest Checkout** and 1-click Express Wallets (Apple Pay, Google Pay, Shop Pay) on mobile, targeting a **5% drop in cart abandonment**.
   - Display transparent shipping calculators directly on the product detail page.
2. **Deploy "Frequently Bought Together" Cart Add-Ons**:
   - Dynamically prompt the high-lift companion item (e.g. prompt the USB-C Hub when a customer adds a Laptop Stand).
   - Projected to lift Average Order Value (AOV) from **$68.40 to $78.30 (+14.5%)**.
3. **Automated Cart Abandonment Recovery**:
   - Trigger a personalized email sequence at 1 hour and 24 hours post-abandonment offering a limited-time free shipping code.
