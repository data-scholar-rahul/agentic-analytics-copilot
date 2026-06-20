INSERT INTO semantic.metric_catalog (
    metric_id,
    metric_name,
    business_definition,
    sql_expression,
    grain,
    default_filters,
    required_tables,
    caveats
)
VALUES
(
    '00000000-0000-0000-0000-000000000001',
    'Revenue',
    'Total payment value for delivered orders. Used as the default commercial revenue metric for this project.',
    'SUM(op.payment_value)',
    'order_id',
    'orders.order_status = ''delivered''',
    ARRAY['mart.orders', 'mart.order_payments'],
    'Olist payment_value may include freight and other payment components depending on source interpretation.'
),
(
    '00000000-0000-0000-0000-000000000002',
    'Order Count',
    'Number of distinct orders.',
    'COUNT(DISTINCT o.order_id)',
    'order_id',
    NULL,
    ARRAY['mart.orders'],
    'Use distinct order_id to avoid overcounting after joins to order_items or payments.'
),
(
    '00000000-0000-0000-0000-000000000003',
    'Average Order Value',
    'Average revenue per order.',
    'SUM(op.payment_value) / NULLIF(COUNT(DISTINCT o.order_id), 0)',
    'order_id',
    'orders.order_status = ''delivered''',
    ARRAY['mart.orders', 'mart.order_payments'],
    'Must use distinct orders to avoid inflated denominator after joins.'
),
(
    '00000000-0000-0000-0000-000000000004',
    'Average Review Score',
    'Average customer review score.',
    'AVG(orev.review_score)',
    'order_id',
    NULL,
    ARRAY['mart.order_reviews'],
    'Not every order may have a review.'
),
(
    '00000000-0000-0000-0000-000000000005',
    'Late Delivery Rate',
    'Percentage of delivered orders where customer delivery timestamp is later than estimated delivery timestamp.',
    'AVG(CASE WHEN o.order_delivered_customer_timestamp > o.order_estimated_delivery_timestamp THEN 1.0 ELSE 0.0 END)',
    'order_id',
    'orders.order_status = ''delivered''',
    ARRAY['mart.orders'],
    'Only meaningful for delivered orders with delivery timestamps.'
),
(
    '00000000-0000-0000-0000-000000000006',
    'Cancellation Rate',
    'Percentage of orders with canceled status.',
    'AVG(CASE WHEN o.order_status = ''canceled'' THEN 1.0 ELSE 0.0 END)',
    'order_id',
    NULL,
    ARRAY['mart.orders'],
    'Should be interpreted over a clearly defined time period.'
),
(
    '00000000-0000-0000-0000-000000000007',
    'Average Delivery Time Days',
    'Average number of days between order purchase timestamp and customer delivery timestamp.',
    'AVG(EXTRACT(EPOCH FROM (o.order_delivered_customer_timestamp - o.order_purchase_timestamp)) / 86400.0)',
    'order_id',
    'orders.order_status = ''delivered''',
    ARRAY['mart.orders'],
    'Requires non-null purchase and delivered customer timestamps.'
)
ON CONFLICT (metric_name) DO UPDATE SET
    business_definition = EXCLUDED.business_definition,
    sql_expression = EXCLUDED.sql_expression,
    grain = EXCLUDED.grain,
    default_filters = EXCLUDED.default_filters,
    required_tables = EXCLUDED.required_tables,
    caveats = EXCLUDED.caveats;


INSERT INTO semantic.table_catalog (
    table_id,
    schema_name,
    table_name,
    business_description,
    grain
)
VALUES
(
    '10000000-0000-0000-0000-000000000001',
    'mart',
    'orders',
    'One row per order with order lifecycle timestamps and order status.',
    'order_id'
),
(
    '10000000-0000-0000-0000-000000000002',
    'mart',
    'order_items',
    'One row per item within an order, including product, seller, price, freight, and shipping limit timestamp.',
    'order_id, order_item_id'
),
(
    '10000000-0000-0000-0000-000000000003',
    'mart',
    'order_payments',
    'One row per payment record for an order, including payment type, installments, and payment value.',
    'order_id, payment_sequential'
),
(
    '10000000-0000-0000-0000-000000000004',
    'mart',
    'order_reviews',
    'Customer review information by order, including review score and optional review comments.',
    'review_id'
),
(
    '10000000-0000-0000-0000-000000000005',
    'mart',
    'customers',
    'Customer identifier and location attributes.',
    'customer_id'
),
(
    '10000000-0000-0000-0000-000000000006',
    'mart',
    'sellers',
    'Seller identifier and location attributes.',
    'seller_id'
),
(
    '10000000-0000-0000-0000-000000000007',
    'mart',
    'products',
    'Product identifier, category, and physical/product metadata.',
    'product_id'
),
(
    '10000000-0000-0000-0000-000000000008',
    'mart',
    'product_category_translation',
    'Mapping from Portuguese product category names to English category names.',
    'product_category_name'
)
ON CONFLICT (schema_name, table_name) DO UPDATE SET
    business_description = EXCLUDED.business_description,
    grain = EXCLUDED.grain;


INSERT INTO semantic.join_rules (
    join_rule_id,
    left_schema,
    left_table,
    left_column,
    right_schema,
    right_table,
    right_column,
    relationship_type,
    business_description
)
VALUES
(
    '20000000-0000-0000-0000-000000000001',
    'mart', 'orders', 'customer_id',
    'mart', 'customers', 'customer_id',
    'many-to-one',
    'Use this join to connect orders to customer location and customer identity attributes.'
),
(
    '20000000-0000-0000-0000-000000000002',
    'mart', 'orders', 'order_id',
    'mart', 'order_items', 'order_id',
    'one-to-many',
    'Use this join to analyze products, sellers, item price, and freight by order.'
),
(
    '20000000-0000-0000-0000-000000000003',
    'mart', 'orders', 'order_id',
    'mart', 'order_payments', 'order_id',
    'one-to-many',
    'Use this join to analyze payment value, payment type, and payment installments by order.'
),
(
    '20000000-0000-0000-0000-000000000004',
    'mart', 'orders', 'order_id',
    'mart', 'order_reviews', 'order_id',
    'one-to-many',
    'Use this join to connect orders with customer review scores and review comments.'
),
(
    '20000000-0000-0000-0000-000000000005',
    'mart', 'order_items', 'product_id',
    'mart', 'products', 'product_id',
    'many-to-one',
    'Use this join to connect order items to product category and product attributes.'
),
(
    '20000000-0000-0000-0000-000000000006',
    'mart', 'order_items', 'seller_id',
    'mart', 'sellers', 'seller_id',
    'many-to-one',
    'Use this join to connect order items to seller location and seller identity attributes.'
),
(
    '20000000-0000-0000-0000-000000000007',
    'mart', 'products', 'product_category_name',
    'mart', 'product_category_translation', 'product_category_name',
    'many-to-one',
    'Use this join to translate product category names from Portuguese to English.'
)
ON CONFLICT (join_rule_id) DO UPDATE SET
    left_schema = EXCLUDED.left_schema,
    left_table = EXCLUDED.left_table,
    left_column = EXCLUDED.left_column,
    right_schema = EXCLUDED.right_schema,
    right_table = EXCLUDED.right_table,
    right_column = EXCLUDED.right_column,
    relationship_type = EXCLUDED.relationship_type,
    business_description = EXCLUDED.business_description;


INSERT INTO semantic.business_glossary (
    glossary_id,
    term,
    definition,
    example
)
VALUES
(
    '30000000-0000-0000-0000-000000000001',
    'Revenue',
    'Default revenue means total payment value for delivered orders.',
    'Monthly revenue is calculated by summing payment_value for delivered orders by purchase month.'
),
(
    '30000000-0000-0000-0000-000000000002',
    'Delivered Order',
    'An order whose order_status is delivered.',
    'Delivered orders are used for delivery time and late delivery calculations.'
),
(
    '30000000-0000-0000-0000-000000000003',
    'Late Delivery',
    'A delivered order where the customer delivery timestamp is later than the estimated delivery timestamp.',
    'If delivered_customer_timestamp > estimated_delivery_timestamp, the order is late.'
),
(
    '30000000-0000-0000-0000-000000000004',
    'Seller Performance',
    'A business concept combining seller revenue, order count, review score, cancellation behavior, and delivery performance.',
    'A high revenue seller with poor review scores and high late delivery rate may require investigation.'
),
(
    '30000000-0000-0000-0000-000000000005',
    'Product Category',
    'A product grouping used to analyze sales and customer experience across types of products.',
    'Product category performance may include revenue, order count, review score, and late delivery rate.'
)
ON CONFLICT (term) DO UPDATE SET
    definition = EXCLUDED.definition,
    example = EXCLUDED.example;