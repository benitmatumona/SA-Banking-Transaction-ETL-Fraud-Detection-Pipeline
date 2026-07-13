import random
import os
import itertools
import pandas as pd
from datetime import datetime
from faker import Faker


data = pd.read_csv("customers.csv")
fake = Faker()
os.makedirs("data/raw", exist_ok=True)
account_id = itertools.count(start=200001)


new_data = {"account_id": [], "customer_id": [], "account_type": [], "open_date": []}

for row in data.itertuples():
    account_types = ["Cheque", "Savings", "Credit"]
    random_number_of_accounts = random.randint(1, 3)
    random_accounts = random.sample(account_types, random_number_of_accounts)

    for account_type in random_accounts:
        start_date = datetime.strptime(row.join_date, "%Y-%m-%d")
        end_date = datetime.strptime("2026-06-01", "%Y-%m-%d")
        open_date = fake.date_between(start_date, end_date)
        (new_data["account_id"].append(next(account_id)),)
        new_data["customer_id"].append(row.customer_id)
        (new_data["account_type"].append(account_type),)
        new_data["open_date"].append(open_date)

df = pd.DataFrame(new_data)
df.to_csv("data/raw/accounts.csv", index=False)
