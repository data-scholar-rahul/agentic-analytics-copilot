CREATE SCHEMA IF NOT EXISTS mart;

DROP TABLE IF EXISTS mart.customers;
CREATE TABLE mart.customers AS
SELECT
    customer_id,
    customer_unique_id,
    NULLIF(customer_zip_code_prefix, '')::INTEGER AS customer_zip_code_prefix,
    customer_city,
    customer_state
FROM raw.olist_customers;

DROP TABLE IF EXISTS mart.geolocation;
CREATE TABLE mart.geolocation AS
SELECT
    NULLIF(geolocation_zip_code_prefix, '')::INTEGER AS geolocation_zip_code_prefix,
    NULLIF(geolocation_lat, '')::DOUBLE PRECISION AS geolocation_lat,
    NULLIF(geolocation_lng, '')::DOUBLE PRECISION AS geolocation_lng,
    geolocation_city,
    geolocation_state
FROM raw.olist_geolocation;

DROP TABLE IF EXISTS mart.order_items;
CREATE TABLE mart.order_items AS
SELECT
    order_id,
    NULLIF(order_item_id, '')::INTEGER AS order_item_id,
    product_id,
    seller_id,
    NULLIF(shipping_limit_date, '')::TIMESTAMP AS shipping_limit_timestamp,
    NULLIF(price, '')::NUMERIC(12, 2) AS price,
    NULLIF(freight_value, '')::NUMERIC(12, 2) AS freight_value
FROM raw.olist_order_items;

DROP TABLE IF EXISTS mart.order_payments;
CREATE TABLE mart.order_payments AS
SELECT
    order_id,
    NULLIF(payment_sequential, '')::INTEGER AS payment_sequential,
    payment_type,
    NULLIF(payment_installments, '')::INTEGER AS payment_installments,
    NULLIF(payment_value, '')::NUMERIC(12, 2) AS payment_value
FROM raw.olist_order_payments;

DROP TABLE IF EXISTS mart.order_reviews;
CREATE TABLE mart.order_reviews AS
SELECT
    review_id,
    order_id,
    NULLIF(review_score, '')::INTEGER AS review_score,
    review_comment_title,
    review_comment_message,
    NULLIF(review_creation_date, '')::TIMESTAMP AS review_creation_timestamp,
    NULLIF(review_answer_timestamp, '')::TIMESTAMP AS review_answer_timestamp
FROM raw.olist_order_reviews;

DROP TABLE IF EXISTS mart.orders;
CREATE TABLE mart.orders AS
SELECT
    order_id,
    customer_id,
    order_status,
    NULLIF(order_purchase_timestamp, '')::TIMESTAMP AS order_purchase_timestamp,
    NULLIF(order_approved_at, '')::TIMESTAMP AS order_approved_timestamp,
    NULLIF(order_delivered_carrier_date, '')::TIMESTAMP AS order_delivered_carrier_timestamp,
    NULLIF(order_delivered_customer_date, '')::TIMESTAMP AS order_delivered_customer_timestamp,
    NULLIF(order_estimated_delivery_date, '')::TIMESTAMP AS order_estimated_delivery_timestamp
FROM raw.olist_orders;

DROP TABLE IF EXISTS mart.products;
CREATE TABLE mart.products AS
SELECT
    product_id,
    product_category_name,
    NULLIF(product_name_lenght, '')::INTEGER AS product_name_length,
    NULLIF(product_description_lenght, '')::INTEGER AS product_description_length,
    NULLIF(product_photos_qty, '')::INTEGER AS product_photos_qty,
    NULLIF(product_weight_g, '')::INTEGER AS product_weight_g,
    NULLIF(product_length_cm, '')::INTEGER AS product_length_cm,
    NULLIF(product_height_cm, '')::INTEGER AS product_height_cm,
    NULLIF(product_width_cm, '')::INTEGER AS product_width_cm
FROM raw.olist_products;

DROP TABLE IF EXISTS mart.sellers;
CREATE TABLE mart.sellers AS
SELECT
    seller_id,
    NULLIF(seller_zip_code_prefix, '')::INTEGER AS seller_zip_code_prefix,
    seller_city,
    seller_state
FROM raw.olist_sellers;

DROP TABLE IF EXISTS mart.product_category_translation;
CREATE TABLE mart.product_category_translation AS
SELECT
    product_category_name,
    product_category_name_english
FROM raw.product_category_name_translation;