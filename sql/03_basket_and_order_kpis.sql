-- =====================================================================
-- Project: E-Commerce Product Funnel & Basket Analysis
-- Script 03: Market Basket KPIs & Co-Purchasing Affinity Extraction
-- Uses: Self-Joins, Aggregate Counts, Co-occurrence Matrix
-- Objective: Discover frequent item pairs and formulate bundling suggestions
-- =====================================================================

USE ecommerce_analytics_db;

-- 1. Macro Order Basket KPIs
SELECT 
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(item_count) AS total_units_sold,
    ROUND(AVG(item_count), 2) AS avg_items_per_basket,
    ROUND(AVG(total_amount), 2) AS average_order_value_aov,
    ROUND(SUM(CASE WHEN item_count > 1 THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) AS multi_item_order_rate_pct
FROM orders;

-- 2. Top Co-Purchased Product Pairs (Self-Join on Order Items)
-- Finds products frequently bought in the exact same transaction basket
SELECT 
    a.product_name AS product_a,
    b.product_name AS product_b,
    COUNT(*) AS co_purchase_frequency,
    ROUND(AVG(a.unit_price + b.unit_price), 2) AS combined_bundle_retail_price
FROM order_items a
JOIN order_items b 
    ON a.order_id = b.order_id 
    AND a.product_id < b.product_id -- Prevents duplicate mirrored pairs (A+B vs B+A)
GROUP BY a.product_name, b.product_name
HAVING co_purchase_frequency >= 150
ORDER BY co_purchase_frequency DESC
LIMIT 10;

-- 3. Category Cross-Selling Distribution
SELECT 
    a.category AS category_a,
    b.category AS category_b,
    COUNT(*) AS cross_category_affinity_count
FROM order_items a
JOIN order_items b 
    ON a.order_id = b.order_id 
    AND a.category <= b.category
WHERE a.category != b.category
GROUP BY a.category, b.category
ORDER BY cross_category_affinity_count DESC;
