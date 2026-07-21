import logging
import pandas as pd
import psycopg2
from psycopg2.extensions import cursor


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def load(
    customers_df: pd.DataFrame,
    accounts_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
) -> None:
    
    conn = None
    
    try:
        conn = connect(database, username, password, "localhost")

        with conn.cursor() as cur:
            load_customers(customers_df, cur)
            load_accounts(accounts_df, cur)
            load_transactions(transactions_df, cur)
            conn.commit()
            logging.info("Data successfully loaded into PostgreSQL.")

    except Exception as e:
        if conn:
            conn.rollback()
        logging.exception(f"Database load failed. {e}")

    finally:
        if conn:
            conn.close()


def connect(
    database: str, 
    username: str, 
    password:str, 
    host: str,
) -> psycopg2.extensions.connection:
    conn = psycopg2.connect(
        dbname=database, user=username, password=password, host=host
    )
    return conn


def load_customers(df: pd.DataFrame, cur: cursor) -> None:
    
    for row in df.itertuples():
        cur.execute(
            """
            INSERT INTO customers (customer_id, full_name, province, join_date)
            VALUES (%s, %s, %s, %s)
            """,
            (row.customer_id, row.full_name, row.province, row.join_date),
        )


def load_accounts(accounts_df: pd.DataFrame, cur: cursor) -> None:    
    for row in accounts_df.itertuples():
        cur.execute(
            """
            INSERT INTO accounts (account_id, customer_id, account_type, open_date)
            VALUES (%s, %s, %s, %s)
            """,
            (row.account_id, row.customer_id, row.account_type, row.open_date),
        )


def load_transactions(transactions_df: pd.DataFrame, cur: cursor) -> None:
    for row in transactions_df.itertuples():
        cur.execute(
            """
            INSERT INTO transactions (transaction_id, account_id, transaction_date, transaction_type,
            transaction_channel, merchant_name, amount, reference, balance_after_transaction, is_fraud)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row.transaction_id,
                row.account_id,
                row.transaction_date,
                row.transaction_type,
                row.transaction_channel,
                row.merchant_name,
                row.amount,
                row.reference,
                row.balance_after_transaction,
                row.is_fraud,
            ),
        )


if __name__ == "__main__":
    customers_df = pd.read_csv("data/raw/customers.csv")
    accounts_df = pd.read_csv("data/raw/accounts.csv")
    transactions_df = pd.read_csv("data/raw/transactions.csv")

    username = "postgres"
    password = ""
    database = "south_africa_bank"

    load(customers_df, accounts_df, transactions_df)
