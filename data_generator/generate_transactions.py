import random
import itertools
import os
import pandas as pd
from typing import Any
from faker import Faker
from src.config import TRANSACTION_CHANNELS, TRANSACTION_TYPES, MERCHANTS


def generate_transactions(
    data: pd.DataFrame,
    fake: Faker,
    transaction_id: int
) -> pd.DataFrame:
    new_data: dict[str, list[Any]] = {
        "transaction_id": [],
        "account_id": [],
        "transaction_date": [],
        "transaction_type": [],
        "transaction_channel": [],
        "merchant_name": [],
        "amount": [],
        "reference": [],
        "balance_after_transaction": [],
        "is_fraud": [],
    }
    
    for row in data.itertuples():
        random_number_of_transactions = random.randint(3, 10)
        end_date = pd.Timestamp.today()
        balance = random_number_of_transactions * 5001

        for _ in range(random_number_of_transactions):
            amount = random.choices(
            population=[
                random.randint(20, 300),
                random.randint(301, 1000),
                random.randint(1001, 5000),
            ],
            weights=[70, 25, 5],
            )[0]
            transaction_type = random.choice(tuple(TRANSACTION_TYPES.keys()))
            merchant_name = random.choice(MERCHANTS[transaction_type])
            reference = TRANSACTION_TYPES[transaction_type].replace(
                "merchant_name", merchant_name
            )

            reference = (
                "EFT DEPOSIT"
                if reference == "CASH DEPOSIT" and random.random() > 0.5
                else reference
            )

            transaction_channel = random.choice(TRANSACTION_CHANNELS[transaction_type])
            is_fraud = is_fraud(
                amount,
                transaction_channel,
                transaction_type,
                merchant_name,
            )
            new_data["transaction_id"].append(next(transaction_id))
            new_data["account_id"].append(row.account_id)
            new_data["transaction_date"].append(
                fake.date_time_between(row.open_date, end_date)
            )
            new_data["transaction_type"].append(transaction_type)
            new_data["transaction_channel"].append(transaction_channel)

            new_data["merchant_name"].append(
                merchant_name if transaction_type != "Salary" else "Employer"
            )

            new_data["amount"].append(amount)

            is_incoming = random.random() >= 0.5

            if transaction_type in ("Salary", "Deposit"):
                balance += amount
            elif transaction_type == "EFT":
                if is_incoming:
                    balance += amount
                else:
                    balance -= amount
            else:
                balance -= amount

            new_data["reference"].append(reference)
            new_data["balance_after_transaction"].append(balance)
            new_data["is_fraud"].append(is_fraud)
    return pd.DataFrame(new_data)


def is_fraud(
    amount: int,
    transaction_channel: str,
    transaction_type: str,
    merchant_name: str,
) -> bool:
    if amount > 4500 and transaction_channel == "ATM":
        is_fraud = random.random() <= 0.20
    elif (
        transaction_type == "Card Purchase"
        and merchant_name == "Uber"
        and amount > 3000
    ):
        is_fraud = random.random() <= 0.12
    else:
        is_fraud = random.random() <= 0.02
    return is_fraud

def generate_transactions_file():

    os.makedirs("data/raw", exist_ok=True)
    data = pd.read_csv(
        "data/raw/accounts.csv",
        parse_dates=["open_date"]
    )
    fake = Faker()
    transaction_id = itertools.count(start=300001)
    generated_df = generate_transactions(data)
    generated_df.to_csv("data/raw/transactions.csv", index=False)
    os.makedirs("data/raw", exist_ok=True)


if __name__ == "__main__":
    generate_transactions_file()