import random
import itertools
import pandas as pd
from faker import Faker


data = pd.read_csv("accounts.csv")
fake= Faker()
transaction_id = itertools.count(start=300001)


new_data = {"transaction_id": [], "account_id": [], "transaction_type": [], "amount": []}
transaction_types = ["Deposit", "Withdrawal", "Card Purchase", "EFT", "Salary"]
transaction_channel = ["ATM", "POS", "Online", "Mobile App", "Branch"]
merchant = ["Checkers", "Pick n Pay", "Woolworths", "Uber", "Netflix", "Shell", "Takealot"]


for row in data.itertuples():
    random_number_of_transactions = random.randint(3, 10)
    
    for _ in range(random_number_of_transactions):
        new_data["transaction_id"].append(next(transaction_id)),
        new_data["account_id"].append(row.account_id)
        new_data["transaction_date"].append(open_date <= transaction_date <= 2026-06-30)
        new_data["transaction_type"].append(random.choice(transaction_types)),
        new_data["transaction_channel"].append(random.choice(transaction_types)),
        new_data["merchant_name"].append(random.choice(transaction_types)),
        new_data["amount"].append(random.randint(20, 5000)),
        new_data["reference"].append(random.randint(20, 5000)),
        new_data["balance_after_transaction"].append(random.randint(20, 5000)),
        new_data["is_fraud"].append(random.randint(20, 5000))


df = pd.DataFrame(new_data)
print(df)
