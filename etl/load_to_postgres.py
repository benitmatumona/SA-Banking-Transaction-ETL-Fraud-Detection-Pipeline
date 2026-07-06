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
            "INSERT INTO customers (customer_id, full_name, province, join_date)"
            f"VALUES ({row.customer_id}, {row.full_name}, {row.province}, {row.join_date});"
            )
        
    for row in accounts_df.itertuples():
        cur.execute(
            "INSERT INTO accounts (account_id, customer_id, account_type, open_date)"
            f"VALUES ({row.account_id}, {row.customer_id}, {row.account_type}, {row.open_date});"
            )
        
    for row in transactions_df.itertuples():
        cur.execute(
            "INSERT INTO transactions (account_id, customer_id, account_type, open_date)"
            f"VALUES ({row.transaction_id}, {row.customer_id}, {row.account_type}, {row.open_date});"
            )
        
