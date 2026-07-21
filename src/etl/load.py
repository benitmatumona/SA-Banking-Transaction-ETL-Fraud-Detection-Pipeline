import logging
import pandas as pd
import psycopg2
from psycopg2.extensions import cursor as Cursor
from psycopg2.extras import execute_values
from src.config import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def read_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers_df = pd.read_csv("data/raw/customers.csv")
    accounts_df = pd.read_csv(
        "data/raw/accounts.csv", 
        parse_dates=["open_date"]
    )
    transactions_df = pd.read_csv(
        "data/raw/transactions.csv", 
        parse_dates=["transaction_date"]
    )
    return customers_df, accounts_df, transactions_df


def load(
    customers_df: pd.DataFrame,
    accounts_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
) -> None:
    try:
        with connect(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST) as conn:
            with conn.cursor() as cur:
                logging.info("loading customers...")
                load_customers(customers_df, cur)
                logging.info("loading accounts...")
                load_accounts(accounts_df, cur)
                logging.info("loading transactions...")
                load_transactions(transactions_df, cur)
            
        logging.info("Data successfully loaded into PostgreSQL.")

    except Exception:
        logging.exception("Database load failed.")


def connect(
    database: str, 
    username: str, 
    password:str, 
    host: str,
) -> psycopg2.extensions.connection:
    return psycopg2.connect(
        dbname=database, user=username, password=password, host=host
    )


def load_customers(customers_df: pd.DataFrame, cur: Cursor) -> None:
    values = [
        (row.customer_id, row.full_name, row.province, row.join_date)
        for row in customers_df.itertuples()
    ]
    
    execute_values(
        """
        INSERT INTO customers (customer_id, full_name, province, join_date)
        VALUES %s
        """,
        values,
    )


def load_accounts(accounts_df: pd.DataFrame, cur: Cursor) -> None:    
    for row in accounts_df.itertuples():
        cur.execute(
            """
            INSERT INTO accounts (account_id, customer_id, account_type, open_date)
            VALUES (%s, %s, %s, %s)
            """,
            (row.account_id, row.customer_id, row.account_type, row.open_date),
        )


def load_transactions(transactions_df: pd.DataFrame, cur: Cursor) -> None:
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
    customers_df, accounts_df, transactions_df = read_data()
    load(customers_df, accounts_df, transactions_df)
