import pandas as pd
import psycopg2


customers_df = pd.read_csv("data/raw/customers.csv")
accounts_df = pd.read_csv("data/raw/accounts.csv")
transactions_df = pd.read_csv("data/raw/transactions.csv")

username = "postgres"
password = ""
database = "south_africa_bank"
conn = None



def connect(
    database: str, 
    username: str, 
    password:str, 
    host: str,
):
    conn = psycopg2.connect(
        dbname=database, user=username, password=password, host=host
    )
    return conn


def load_customers():
    raise ValueError


def load_accounts():
    raise ValueError


def load_transactions():
    raise ValueError


def load():
    raise ValueError

try:
    conn = connect(database, username, password, "localhost")

    with conn.cursor() as cur:
        for row in customers_df.itertuples():
            cur.execute(
                """
                INSERT INTO customers (customer_id, full_name, province, join_date)
                VALUES (%s, %s, %s, %s)
                """,
                (row.customer_id, row.full_name, row.province, row.join_date),
            )

        for row in accounts_df.itertuples():
            cur.execute(
                """
                INSERT INTO accounts (account_id, customer_id, account_type, open_date)
                VALUES (%s, %s, %s, %s)
                """,
                (row.account_id, row.customer_id, row.account_type, row.open_date),
            )

        for row in transactions_df.itertuples():
            cur.execute(
                """
                INSERT INTO transactions (transaction_id, account_id, transaction_date, transaction_type,
                merchant_name, amount, reference, balance_after_transaction, is_fraud)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    row.transaction_id,
                    row.account_id,
                    row.transaction_date,
                    row.transaction_type,
                    row.merchant_name,
                    row.amount,
                    row.reference,
                    row.balance_after_transaction,
                    row.is_fraud,
                ),
            )

        conn.commit()
except Exception as e:
    if conn:
        conn.rollback()
    print(e)

finally:
    if conn:
        conn.close()
