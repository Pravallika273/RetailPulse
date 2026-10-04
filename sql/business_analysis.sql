-- ============================================================
-- RETAILPULSE - BUSINESS ANALYSIS SQL
-- ============================================================

-- 1. EXECUTIVE KPIs
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    SUM(quantity) AS total_quantity,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(DISTINCT customer_key) AS identified_customers,
    COUNT(DISTINCT product_key) AS unique_products,
    ROUND(SUM(revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value
FROM retail.fact_sales;


-- 2. MONTHLY SALES
SELECT
    d.year_month,
    ROUND(SUM(f.revenue), 2) AS revenue,
    COUNT(DISTINCT f.invoice_no) AS orders,
    COUNT(DISTINCT f.customer_key) AS customers,
    ROUND(
        SUM(f.revenue) / COUNT(DISTINCT f.invoice_no),
        2
    ) AS average_order_value,
    MAX(d.is_partial_period::int) = 1 AS partial_period
FROM retail.fact_sales f
JOIN retail.dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year_month
ORDER BY d.year_month;


-- 3. TOP 20 PRODUCTS BY REVENUE
SELECT
    p.stock_code,
    p.description,
    ROUND(SUM(f.revenue), 2) AS revenue,
    SUM(f.quantity) AS quantity,
    COUNT(DISTINCT f.invoice_no) AS orders
FROM retail.fact_sales f
JOIN retail.dim_product p
    ON f.product_key = p.product_key
GROUP BY p.stock_code, p.description
ORDER BY revenue DESC
LIMIT 20;


-- 4. COUNTRY PERFORMANCE
SELECT
    c.country_name,
    ROUND(SUM(f.revenue), 2) AS revenue,
    COUNT(DISTINCT f.invoice_no) AS orders,
    COUNT(DISTINCT f.customer_key) AS customers,
    ROUND(
        100.0 * SUM(f.revenue) /
        SUM(SUM(f.revenue)) OVER (),
        2
    ) AS revenue_share_pct
FROM retail.fact_sales f
JOIN retail.dim_country c
    ON f.country_key = c.country_key
GROUP BY c.country_name
ORDER BY revenue DESC;


-- 5. TOP CUSTOMERS
SELECT
    c.customer_id,
    ROUND(SUM(f.revenue), 2) AS revenue,
    COUNT(DISTINCT f.invoice_no) AS orders,
    COUNT(DISTINCT f.product_key) AS products
FROM retail.fact_sales f
JOIN retail.dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.customer_id
ORDER BY revenue DESC
LIMIT 20;


-- 6. PRODUCT REVENUE CONCENTRATION
WITH product_revenue AS (
    SELECT
        product_key,
        SUM(revenue) AS revenue
    FROM retail.fact_sales
    GROUP BY product_key
),
ranked AS (
    SELECT
        product_key,
        revenue,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) AS product_rank
    FROM product_revenue
)
SELECT
    COUNT(*) AS total_products,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(
        SUM(revenue) FILTER (WHERE product_rank <= 10),
        2
    ) AS top_10_revenue,
    ROUND(
        100.0 * SUM(revenue) FILTER (WHERE product_rank <= 10)
        / SUM(revenue),
        2
    ) AS top_10_revenue_share_pct
FROM ranked;


-- 7. POTENTIAL TRANSACTION ANOMALIES
SELECT
    p.stock_code,
    p.description,
    SUM(f.quantity) AS quantity,
    ROUND(SUM(f.revenue), 2) AS revenue,
    COUNT(DISTINCT f.invoice_no) AS orders
FROM retail.fact_sales f
JOIN retail.dim_product p
    ON f.product_key = p.product_key
GROUP BY p.stock_code, p.description
HAVING SUM(f.quantity) > 50000
    OR SUM(f.revenue) > 150000
ORDER BY revenue DESC;


-- 8. DATA QUALITY CHECK
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE quantity <= 0) AS invalid_quantity_rows,
    COUNT(*) FILTER (WHERE unit_price <= 0) AS invalid_price_rows,
    COUNT(*) FILTER (WHERE revenue <= 0) AS invalid_revenue_rows,
    COUNT(*) FILTER (WHERE invoice_no IS NULL) AS missing_invoice_rows,
    COUNT(*) FILTER (WHERE product_key IS NULL) AS missing_product_rows,
    COUNT(*) FILTER (WHERE country_key IS NULL) AS missing_country_rows
FROM retail.fact_sales;