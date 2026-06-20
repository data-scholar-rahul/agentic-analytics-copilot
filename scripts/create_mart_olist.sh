#!/usr/bin/env bash
set -e

DB_NAME="analytics_agent"

echo "Creating mart Olist tables..."
psql -d "$DB_NAME" -f backend/sql/002_create_mart_olist_tables.sql

echo "Mart table row counts:"
psql -d "$DB_NAME" -c "
SELECT 'mart.customers' AS table_name, COUNT(*) FROM mart.customers
UNION ALL
SELECT 'mart.geolocation', COUNT(*) FROM mart.geolocation
UNION ALL
SELECT 'mart.order_items', COUNT(*) FROM mart.order_items
UNION ALL
SELECT 'mart.order_payments', COUNT(*) FROM mart.order_payments
UNION ALL
SELECT 'mart.order_reviews', COUNT(*) FROM mart.order_reviews
UNION ALL
SELECT 'mart.orders', COUNT(*) FROM mart.orders
UNION ALL
SELECT 'mart.products', COUNT(*) FROM mart.products
UNION ALL
SELECT 'mart.sellers', COUNT(*) FROM mart.sellers
UNION ALL
SELECT 'mart.product_category_translation', COUNT(*) FROM mart.product_category_translation
ORDER BY table_name;
"