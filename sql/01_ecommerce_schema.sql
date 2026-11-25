-- =====================================================================
-- Project: E-Commerce Product Funnel & Basket Analysis
-- Script 01: Multi-Table Relational Schema Setup
-- Database: MySQL 8.0+
-- Description: Creates sessions, funnel_events, orders, and order_items tables
-- =====================================================================

CREATE DATABASE IF NOT EXISTS ecommerce_analytics_db;
USE ecommerce_analytics_db;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS funnel_events;
DROP TABLE IF EXISTS products;

-- 1. Product Catalog Table
CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    INDEX idx_category (category)
);

-- 2. Customer Clickstream Funnel Events Table
CREATE TABLE funnel_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(30) NOT NULL,
    user_id VARCHAR(30) NOT NULL,
    event_timestamp DATETIME NOT NULL,
    stage_order INT NOT NULL,
    stage_name VARCHAR(50) NOT NULL,
    traffic_source VARCHAR(40) NOT NULL,
    device_category VARCHAR(20) NOT NULL,
    product_id VARCHAR(20),
    INDEX idx_session (session_id),
    INDEX idx_stage (stage_name),
    INDEX idx_device (device_category)
);

-- 3. Completed Orders Table
CREATE TABLE orders (
    order_id VARCHAR(30) PRIMARY KEY,
    session_id VARCHAR(30) NOT NULL,
    user_id VARCHAR(30) NOT NULL,
    order_date DATETIME NOT NULL,
    device_category VARCHAR(20) NOT NULL,
    traffic_source VARCHAR(40) NOT NULL,
    item_count INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    INDEX idx_order_date (order_date),
    INDEX idx_user (user_id)
);

-- 4. Order Line Items (Baskets)
CREATE TABLE order_items (
    order_item_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    INDEX idx_product (product_id)
);

DESCRIBE funnel_events;
DESCRIBE orders;
DESCRIBE order_items;
