#!/usr/bin/env bash
set -e

DB_NAME="analytics_agent"
DATA_DIR="data/olist"

echo "Creating raw Olist tables..."
psql -d "$DB_NAME" -f backend/sql/001_create_raw_olist_tables.sql

echo "Loading CSV files into raw schema..."

psql -d "$DB_NAME" -c "\copy raw.olist_customers FROM '${DATA_DIR}/olist_customers_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"

psql -d "$DB_NAME" -c "\copy raw.olist_geolocation FROM '${DATA_DIR}/olist_geolocation_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"

psql -d "$DB_NAME" -c "\copy raw.olist_order_items FROM '${DATA_DIR}/olist_order_items_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"

psql -d "$DB_NAME" -c "\copy raw.olist_order_payments FROM '${DATA_DIR}/olist_order_payments_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"

psql -d "$DB_NAME" -c "\copy raw.olist_order_reviews FROM '${DATA_DIR}/olist_order_reviews_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"

psql -d "$DB_NAME" -c "\copy raw.olist_orders FROM '${DATA_DIR}/olist_orders_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"

psql -d "$DB_NAME" -c "\copy raw.olist_products FROM '${DATA_DIR}/olist_products_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"

psql -d "$DB_NAME" -c "\copy raw.olist_sellers FROM '${DATA_DIR}/olist_sellers_dataset.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"

psql -d "$DB_NAME" -c "\copy raw.product_category_name_translation FROM '${DATA_DIR}/product_category_name_translation.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '\"')"

echo "Raw load complete."

echo "Row counts:"
psql -d "$DB_NAME" -c "
SELECT 'raw.olist_customers' AS table_name, COUNT(*) FROM raw.olist_customers
UNION ALL
SELECT 'raw.olist_geolocation', COUNT(*) FROM raw.olist_geolocation
UNION ALL
SELECT 'raw.olist_order_items', COUNT(*) FROM raw.olist_order_items
UNION ALL
SELECT 'raw.olist_order_payments', COUNT(*) FROM raw.olist_order_payments
UNION ALL
SELECT 'raw.olist_order_reviews', COUNT(*) FROM raw.olist_order_reviews
UNION ALL
SELECT 'raw.olist_orders', COUNT(*) FROM raw.olist_orders
UNION ALL
SELECT 'raw.olist_products', COUNT(*) FROM raw.olist_products
UNION ALL
SELECT 'raw.olist_sellers', COUNT(*) FROM raw.olist_sellers
UNION ALL
SELECT 'raw.product_category_name_translation', COUNT(*) FROM raw.product_category_name_translation
ORDER BY table_name;
"
