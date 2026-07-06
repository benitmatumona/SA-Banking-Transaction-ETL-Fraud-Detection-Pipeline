import os
import pandas as pd
import psycopg2


customers_df = pd.read_csv("data/raw/customers.csv")
accounts_df = pd.read_csv("data/raw/accounts.csv")
transactions_df = pd.read_csv("data/raw/transactions.csv")

username = "postgres"
password = ""
database = "south_africa_bank"

conn = psycopg2.connect(
    dbname=database,
    user=username,
    password=password,
    host="localhost"
)    

with conn.cursor() as cur:
    for row in customers_df.itertuples():
        cur.execute(
            "INSERT INTO accounts (customer_id, full_name, province, join_date)"
            f"VALUES ({row.customer_id}, {row.full_name}, {row.province}, {row.join_date});"
            )
        
    for row in accounts_df.itertuples():
        cur.execute(
            "INSERT INTO accounts (customer_id, full_name, province, join_date)"
            f"VALUES ({row.customer_id}, {row.full_name}, {row.province}, {row.join_date});"
            )