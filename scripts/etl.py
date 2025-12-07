import pandas as pd
import psycopg2

# -------------------------------------
# 1. PostgreSQL Connection
# -------------------------------------
conn = psycopg2.connect(
    host="localhost",
    database="ecommerce_db",
    user="postgres",
    password="pihuarora"
)
cur = conn.cursor()
print("Connected to PostgreSQL")


# -------------------------------------
# 2. Read CSV file
# -------------------------------------
df = pd.read_csv("data/raw_orders.csv")
print("CSV Loaded Successfully")
print(df.head())


# -------------------------------------
# 3. Insert INTO dim_customer (avoid duplicates)
# -------------------------------------
for index, row in df.iterrows():
    cur.execute("""
        INSERT INTO dim_customer (customer_key, customer_name, customer_email)
        VALUES (%s, %s, %s)
        ON CONFLICT (customer_key) DO NOTHING;
    """, (row['customer_key'], row['customer_name'], row['customer_email']))

conn.commit()
print("dim_customer ✔")


# -------------------------------------
# 4. Insert INTO dim_product (avoid duplicates)
# -------------------------------------
for index, row in df.iterrows():
    cur.execute("""
        INSERT INTO dim_product (product_key, product_name, product_category)
        VALUES (%s, %s, %s)
        ON CONFLICT (product_key) DO NOTHING;
    """, (row['product_key'], row['product_name'], row['product_category']))

conn.commit()
print("dim_product ✔")


# -------------------------------------
# 5. Insert INTO dim_date (avoid duplicates)
# -------------------------------------
for index, row in df.iterrows():
    order_date = pd.to_datetime(row["order_date"])
    year = order_date.year
    month = order_date.month
    day = order_date.day

    cur.execute("""
        INSERT INTO dim_date (order_date, year, month, day)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (order_date) DO NOTHING;
    """, (order_date, year, month, day))


conn.commit()
print("dim_date ✔")


# -------------------------------------
# 6. Now insert into fact_orders
# -------------------------------------
for index, row in df.iterrows():

    # get customer_id
    cur.execute("SELECT customer_id FROM dim_customer WHERE customer_key = %s",
                (row['customer_key'],))
    customer_id = cur.fetchone()[0]

    # get product_id
    cur.execute("SELECT product_id FROM dim_product WHERE product_key = %s",
                (row['product_key'],))
    product_id = cur.fetchone()[0]

    # get date_id
    cur.execute("SELECT date_id FROM dim_date WHERE order_date = %s",
                (row['order_date'],))
    date_id = cur.fetchone()[0]

    # calculate amount
    amount = row['quantity'] * row['unit_price']

    # insert into fact table
    cur.execute("""
        INSERT INTO fact_orders (order_id, customer_id, product_id, date_id, quantity, unit_price, amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING;
    """, (
        row['order_id'], customer_id, product_id, date_id,
        row['quantity'], row['unit_price'], amount
    ))

conn.commit()
print("fact_orders ✔")


# -------------------------------------
# Close connection
# -------------------------------------
cur.close()
conn.close()
print("ETL Completed Successfully 🎉")
