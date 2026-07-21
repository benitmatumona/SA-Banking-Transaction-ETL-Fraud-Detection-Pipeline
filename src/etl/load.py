import logging
import pandas as pd
import psycopg2
from psycopg2.extensions import cursor as Cursor
from psycopg2.extras import execute_values
from src.config import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    CUSTOMER_SQL,
    ACCOUNT_SQL,
    TRANSACTION_SQL

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

    except Exception as e:
        logging.exception(f"Database load failed. {e}")


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
    rows = list(
        customers_df.itertuples(index=False, name=None)
    )
    
    bulk_insert(
        cur,
        CUSTOMER_SQL,
        rows
    )


def load_accounts(accounts_df: pd.DataFrame, cur: Cursor) -> None:    
    rows = list(
        accounts_df.itertuples(index=False, name=None)
    )
    
    bulk_insert(
        cur,
        ACCOUNT_SQL,
        rows
    )


def load_transactions(transactions_df: pd.DataFrame, cur: Cursor) -> None:
    rows = list(
        transactions_df.itertuples(index=False, name=None)
    )
    bulk_insert(    
        cur,
        TRANSACTION_SQL,
        rows
    )


def bulk_insert(
    cur: Cursor,
    sql: str,
    rows: list[tuple],
) -> None:
    execute_values(
        cur,
        sql,
        rows,
        page_size=1000
    )


if __name__ == "__main__":
    customers_df, accounts_df, transactions_df = read_data()
    load(customers_df, accounts_df, transactions_df)