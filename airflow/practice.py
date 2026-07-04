import random
import os
import itertools
import pandas as pd
from datetime import datetime
from faker import Faker


data = pd.read_csv("customers.csv")
fake= Faker()
os.makedirs("data/raw", exist_ok=True)
account_id = itertools.count(start=200001)


with open("data/raw/accounts.csv", "w") as f:
    for customer_id, customer_date in zip(data["customer_id"], data["join_date"]):
        account_types = ["Cheque", "Savings", "Credit"]
        random_number_of_accounts = random.randint(1, 3)
        random_accounts = random.sample(account_type, random_number_of_accounts)
        
        for account_type in random_accounts:
            start_date = datetime.strptime(customer_date, "%y-%m-%d")
            end_date = datetime.strptime("2026-06-01", "%y-%m-%d")
            open_date = fake.date_between(start_date, end_date)
            f.write(f"{next(account_id)},{customer_id},{account_type},{open_date}\n")
 