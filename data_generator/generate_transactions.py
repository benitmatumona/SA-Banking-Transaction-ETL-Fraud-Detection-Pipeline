import random
import itertools
import os
import pandas as pd
from datetime import datetime
from faker import Faker


os.makedirs("data/raw", exist_ok=True)
data = pd.read_csv("data/raw/accounts.csv")
fake = Faker()
transaction_id = itertools.count(start=300001)


new_data = {
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
transaction_types = {
    "Deposit": "CASH DEPOSIT",
    "Withdrawal": "ATM CASH WITHDRAWAL",
    "Card Purchase": "merchant_name",
    "EFT": "EFT TO merchant_name",
    "Salary": "MONTHLY SALARY",
}
transaction_channel = ["ATM", "POS", "Online", "Mobile App", "Branch"]

merchant = {
    "Deposit": ["This Bank"],
    "Withdrawal": ["This Bank"],
    "Card Purchase": [
        "Checkers",
        "Pick n Pay",
        "Woolworths",
        "Uber",
        "Netflix",
        "Shell",
        "Takealot",
    ],
    "EFT": [
        "SARS",
        "Municipality",
        "Landlord",
        "Checkers",
        "Pick n Pay",
        "Woolworths",
        "Uber",
        "Netflix",
        "Shell",
        "Takealot",
    ],
    "Salary": ["Employer"],
}

for row in data.itertuples():
    random_number_of_transactions = random.randint(3, 10)
    open_date = datetime.strptime(row.open_date, "%Y-%m-%d")
    end_date = pd.Timestamp.today()
    balance = random_number_of_transactions * 5001

    for _ in range(random_number_of_transactions):
        amount = random.randint(20, 5000)
        transaction_type = random.choice(list(transaction_types.keys()))
        merchant_name = random.choice(merchant[transaction_type])
        reference = transaction_types[transaction_type].replace(
            "merchant_name", merchant_name
        )
        reference = (
            "EFT DEPOSIT"
            if reference == "CASH DEPOSIT" and random.random() > 0.5
            else reference
        )
        is_fraud = random.random() > 0.98

        (new_data["transaction_id"].append(next(transaction_id)),)
        new_data["account_id"].append(row.account_id)
        new_data["transaction_date"].append(fake.date_between(open_date, end_date))
        (new_data["transaction_type"].append(transaction_type),)
        (new_data["transaction_channel"].append(random.choice(transaction_channel)),)
        (
            new_data["merchant_name"].append(
                merchant_name if transaction_type != "Salary" else "Employer"
            ),
        )
        (new_data["amount"].append(amount),)

        if transaction_type in ["Salary", "Deposit"]:
            balance += amount
        elif transaction_type == "EFT" and random.random() >= 0.5:
            balance += amount
        else:
            balance -= amount

        (new_data["reference"].append(reference),)
        (new_data["balance_after_transaction"].append(balance),)
        new_data["is_fraud"].append(is_fraud)


df = pd.DataFrame(new_data)
df.to_csv("data/raw/transactions.csv", index=False)
