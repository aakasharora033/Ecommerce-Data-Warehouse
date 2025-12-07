# 🛒 E-Commerce Data Warehouse & ETL Pipeline

### **Tech Stack:** Python (pandas, psycopg2), PostgreSQL, PgAdmin, SQL, Git/GitHub  
### **Objective:** Build a complete end-to-end ETL pipeline + star schema data warehouse for analytics.

---

## 📌 Project Summary

This project simulates a real-world e-commerce analytics pipeline.  
It takes **raw order-level CSV data**, processes it using Python, and loads it into a **PostgreSQL data warehouse** designed using a **Star Schema**.

The system supports analytics such as:

- Top-selling products  
- Monthly revenue trends  
- Customer spending patterns  
- Category-level performance  

---

## 📂 Repository Structure

```
ECOMMERCE-Data-Warehouse/
│
├── data/
│   └── raw_orders.csv
│
├── docs/
│   └── screenshots/
│       ├── tables_list.png
│       ├── fact_structure.png
│       └── fact_order_data.png
│
├── scripts/
│   └── etl.py
│
├── sql/
│   ├── schema.sql
│   └── analysis.sql
│
└── README.md
```

---

## ⭐ System Architecture

```mermaid
flowchart LR
    A[Raw CSV (raw_orders.csv)]
    --> B[Python ETL (pandas + psycopg2)]
    --> C[PostgreSQL Data Warehouse]
    --> D[Fact & Dimension Tables]
    --> E[Analytics Queries (SQL)]
```

## 🧱 Star Schema Design

### **Dimension Tables**
- `dim_customer`
- `dim_product`
- `dim_date`

### **Fact Table**
- `fact_orders`  
  Contains foreign keys referencing all dimensions.

This allows efficient analytical queries.

---

## ⚙️ ETL Pipeline Workflow

1. Load raw CSV with pandas  
2. Insert/Upsert into dimension tables  
3. Extract surrogate keys  
4. Load into fact table with calculated metrics (e.g., amount = price × quantity)  
5. Validate data in PgAdmin  

✔ Idempotent inserts  
✔ Duplicate-safe  
✔ Fully automated load

---

## 📊 Example Analytics Queries (from analysis.sql)

### **1️⃣ Top Products**
```sql
SELECT p.product_name, SUM(f.quantity) AS total_qty
FROM fact_orders f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_qty DESC
LIMIT 10;
```

### **2️⃣ Monthly Revenue Trend**
```sql
SELECT d.year, d.month, SUM(f.amount) AS revenue
FROM fact_orders f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;
```

### **3️⃣ Top Customers by Spending**
```sql
SELECT c.customer_name, SUM(f.amount) AS total_spent
FROM fact_orders f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_spent DESC;
```

---

## 🧠 What I Learned

- Designing a **star schema**  
- Building an end-to-end **ETL pipeline**  
- Python → PostgreSQL data loading  
- Surrogate key mapping  
- Writing analytical SQL  
- Using PgAdmin for visual schema inspection  
- Structuring a production-style data engineering project

---

## 🚀 Future Improvements

- Add Airflow DAG for scheduling  
- Introduce S3 > ETL > Redshift flow  
- Add data validation layer  
- Use DBT for transformation modelling  
- Add dashboards (Power BI / Tableau)

---

If you like this project, ⭐ the repo!
