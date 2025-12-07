-- sql/analysis.sql

-- Top 10 products by quantity sold
SELECT p.product_name, SUM(f.quantity) AS total_qty
FROM fact_orders f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_qty DESC
LIMIT 10;

-- Monthly revenue
SELECT d.year, d.month, SUM(f.amount) AS revenue
FROM fact_orders f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- Top customers by revenue
SELECT c.customer_name, SUM(f.amount) AS total_spent
FROM fact_orders f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_spent DESC
LIMIT 10;

-- Category-wise sales
SELECT p.product_category, SUM(f.quantity) AS qty, SUM(f.amount) AS revenue
FROM fact_orders f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_category
ORDER BY revenue DESC;
