-- sql/schema.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id SERIAL PRIMARY KEY,
    customer_key VARCHAR(100) UNIQUE,
    customer_name VARCHAR(150),
    customer_email VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id SERIAL PRIMARY KEY,
    product_key VARCHAR(100) UNIQUE,
    product_name VARCHAR(150),
    product_category VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id SERIAL PRIMARY KEY,
    order_date DATE UNIQUE,
    year INT,
    month INT,
    day INT
);

CREATE TABLE IF NOT EXISTS fact_orders (
    order_id VARCHAR(100) PRIMARY KEY,
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    date_id INT REFERENCES dim_date(date_id),
    quantity INT,
    unit_price NUMERIC(12,2),
    amount NUMERIC(12,2)
);
