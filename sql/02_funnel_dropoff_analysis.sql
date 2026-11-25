-- =====================================================================
-- Project: E-Commerce Product Funnel & Basket Analysis
-- Script 02: Funnel Conversion & Abandonment Drop-Off Analysis
-- Uses: CTEs, Window Functions (LAG), Conditional Aggregations
-- Objective: Uncover the 18% abandonment drop-off between Cart and Checkout
-- =====================================================================

USE ecommerce_analytics_db;

-- 1. End-to-End Funnel Progression with Stage-to-Stage Drop-off Rates
WITH stage_session_counts AS (
    SELECT 
        stage_order,
        stage_name,
        COUNT(DISTINCT session_id) AS total_sessions
    FROM funnel_events
    GROUP BY stage_order, stage_name
),
funnel_with_lag AS (
    SELECT 
        stage_order,
        stage_name,
        total_sessions,
        -- Window function: Fetch sessions from immediately preceding funnel stage
        LAG(total_sessions) OVER (ORDER BY stage_order) AS previous_stage_sessions,
        -- Initial top-of-funnel traffic (Home Page View)
        FIRST_VALUE(total_sessions) OVER (ORDER BY stage_order) AS top_of_funnel_sessions
    FROM stage_session_counts
)
SELECT 
    stage_order,
    stage_name,
    total_sessions,
    -- Conversion as % of initial home page visitors
    ROUND((total_sessions * 100.0) / top_of_funnel_sessions, 2) AS overall_conversion_pct,
    -- Step-by-step abandonment drop-off
    CASE 
        WHEN previous_stage_sessions IS NULL THEN 0.00
        ELSE ROUND(((previous_stage_sessions - total_sessions) * 100.0) / previous_stage_sessions, 2)
    END AS step_dropoff_pct
FROM funnel_with_lag
ORDER BY stage_order;

-- 2. Granular Cart-to-Checkout Abandonment Isolation by Device Type
-- Validates why mobile exhibits the highest drop-off
WITH device_stage_counts AS (
    SELECT 
        device_category,
        COUNT(DISTINCT CASE WHEN stage_name = '3_Add_to_Cart' THEN session_id END) AS cart_sessions,
        COUNT(DISTINCT CASE WHEN stage_name = '4_Initiate_Checkout' THEN session_id END) AS checkout_sessions
    FROM funnel_events
    GROUP BY device_category
)
SELECT 
    device_category,
    cart_sessions,
    checkout_sessions,
    (cart_sessions - checkout_sessions) AS abandoned_carts,
    -- Calculate drop-off rate
    ROUND(((cart_sessions - checkout_sessions) * 100.0) / cart_sessions, 2) AS cart_abandonment_dropoff_pct
FROM device_stage_counts
ORDER BY cart_abandonment_dropoff_pct DESC;

-- 3. Traffic Source Conversion Performance to Checkout
SELECT 
    traffic_source,
    COUNT(DISTINCT session_id) AS total_visitors,
    COUNT(DISTINCT CASE WHEN stage_name = '3_Add_to_Cart' THEN session_id END) AS cart_adds,
    COUNT(DISTINCT CASE WHEN stage_name = '4_Initiate_Checkout' THEN session_id END) AS checkouts,
    COUNT(DISTINCT CASE WHEN stage_name = '5_Complete_Purchase' THEN session_id END) AS completed_purchases,
    ROUND(COUNT(DISTINCT CASE WHEN stage_name = '5_Complete_Purchase' THEN session_id END) * 100.0 / COUNT(DISTINCT session_id), 2) AS overall_traffic_roi_pct
FROM funnel_events
GROUP BY traffic_source
ORDER BY overall_traffic_roi_pct DESC;
