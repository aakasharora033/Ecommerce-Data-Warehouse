# E-Commerce Data Warehouse & ETL Pipeline

**One-line:** End-to-end ETL pipeline that ingests raw e-commerce order CSV into a PostgreSQL star schema (fact + dimension tables) and exposes analytics queries.

## Project Summary
Built a simple, production-style data pipeline using Python (pandas + psycopg2) and PostgreSQL. The pipeline:
- Loads raw CSV orders,
- Upserts dimension tables (`dim_customer`, `dim_product`, `dim_date`),
- Populates `fact_orders` with surrogate keys,
- Provides analytical SQL queries for insights (top products, monthly revenue, customer spend).

**Tech:** Python, pandas, psycopg2, PostgreSQL, PgAdmin (optional), Git/GitHub

## Repo Structure
ECOMMERCE/
├── data/
│ └── raw_orders.csv
├── scripts/
│ └── etl.py
├── sql/
│ ├── schema.sql
│ └── analysis.sql
├── docs/
│ └── screenshots/
└── README.md

## Architecture (Mermaid)
```mermaid
flowchart LR
  A[raw_orders.csv] --> B[Python ETL (pandas)]
  B --> C[PostgreSQL Dim Tables]
  C --> D[fact_orders]
  D --> E[Analytics Queries / BI]


How to run (local)

Create & configure DB (see sql/schema.sql)

Put raw_orders.csv into data/

Install env: pip install -r requirements.txt

Run: python scripts/etl.py

Verify in PgAdmin: SELECT * FROM fact_orders;

SQL Schema

See sql/schema.sql for full CREATE TABLE statements (star schema).

Example Analytics Queries

See sql/analysis.sql — includes top products, monthly revenue and top customers queries.

What I learned

Designing star schema (fact + dims)

Building idempotent ETL with upserts

Mapping natural keys → surrogate keys

Writing production-style SQL for analytics

Next improvements

Add Airflow DAG for orchestration

Move data storage to cloud (S3 + BigQuery/Redshift)

Add unit tests & logging


(When pasting, keep the triple backticks for mermaid so GitHub will render.)

---

## 2) `sql/schema.sql` — paste this file (if not already saved)

```sql
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
