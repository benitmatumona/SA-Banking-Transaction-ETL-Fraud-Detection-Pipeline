import random
import pandas as pd
import itertools
from datetime import datetime
from faker import Faker


data = pd.read_csv("accounts.csv")
fake= Faker()
transaction_id = itertools.count(start=300001)


new_data = {"transaction_id": [], "account_id": [], "transaction_date": [], 
            "transaction_type": [], "transaction_channel": [], "merchant_name": [], 
            "amount": [], "reference": [], "balance_after_transaction": [], "is_fraud": []}
transaction_types = {"Deposit": "CASH DEPOSIT", "Withdrawal": "ATM CASH WITHDRAWAL", 
                     "Card Purchase": "merchant_name", "EFT": "EFT TO merchant_name", 
                     "Salary": "MONTHLY SALARY"}
transaction_channel = ["ATM", "POS", "Online", "Mobile App", "Branch"]
merchant = ["Checkers", "Pick n Pay", "Woolworths", "Uber", "Netflix", "Shell", "Takealot"]


for row in data.itertuples():
    random_number_of_transactions = random.randint(3, 10)
    open_date = datetime.strptime(row.open_date, "%Y-%m-%d")
    end_date = datetime.strptime("2026-06-30", "%Y-%m-%d")
    
    for _ in range(random_number_of_transactions):
        balance = random_number_of_transactions * 5001
        amount = random.randint(20, 5000)
        merchant_name = random.choice(merchant)
        transaction_type = random.choice(transaction_types.keys())
        reference = transaction_types[transaction_type].replace("merchant_name", merchant_name)
        reference = "EFT DEPOSIT" if reference == "CASH DEPOSIT" and random.random() > 0.5 else reference
        is_fraud = random.random() > 0.9

        new_data["transaction_id"].append(next(transaction_id)),
        new_data["account_id"].append(row.account_id)
        new_data["transaction_date"].append(fake.date_between(open_date, end_date))
        new_data["transaction_type"].append(random.choice(transaction_types.keys())),
        new_data["transaction_channel"].append(random.choice(transaction_channel)),
        new_data["merchant_name"].append(merchant_name),
        new_data["amount"].append(amount),
        new_data["reference"].append(reference),
        new_data["balance_after_transaction"].append(
            balance + amount if transaction_type == "Salary" else balance - amount
            ),
        new_data["is_fraud"].append(is_fraud)


df = pd.DataFrame(new_data)
