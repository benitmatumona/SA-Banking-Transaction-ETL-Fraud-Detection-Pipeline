import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)
customers_df = pd.read_csv("data/raw/customers.csv")
accounts_df = pd.read_csv("data/raw/accounts.csv")
transactions_df = pd.read_csv("data/raw/transactions.csv")


def check_duplicates(df: pd.DataFrame, column_name: str) -> bool:
    if df[column_name].duplicated().any():
        raise ValueError(f"Duplicate values found in '{column_name}'.")
    return True


def check_missing_values(df: pd.DataFrame, required_columns: list[str]) -> bool:

    for column in required_columns:
        if df[column].isnull().any():
            raise ValueError(f"Missing values found in '{column}'.")
    return True


def check_allowed_types(
    df: pd.DataFrame, column_name: str, allowed_types: list[str]
) -> bool:
    valid_mask: list[bool] = df[column_name].isin(allowed_types)
    invalid_values = set()

    for value, is_valid in zip(df[column_name], valid_mask):
        if not is_valid:
            invalid_values.add(value)
    if invalid_values:
        raise ValueError(f"Invalid {column_name} found '{sorted(invalid_values)}'.")
    return True


def check_transaction_amounts(df: pd.DataFrame) -> bool:
    Max_TRANSACTION_AMOUNT = 10_000_000

    if (df["amount"].isna()).any():
        raise ValueError(f"Missing values found in the column 'amount'.")
    if (df["amount"] <= 0).any():
        raise ValueError("Transaction amounts must be greater than 0.")
    if (df["amount"] > Max_TRANSACTION_AMOUNT).any():
        raise ValueError("Transaction amounts cannot be greater than 10 000 000.")
    return True


def check_transaction_dates(
    transactions_df: pd.DataFrame, accounts_df: pd.DataFrame
) -> bool:
    df = pd.merge(
        transactions_df[["transaction_id", "account_id", "transaction_date"]],
        accounts_df[["account_id", "open_date"]],
        on="account_id",
        how="inner",
    )
    transaction_date = pd.to_datetime(df["transaction_date"])
    open_date = pd.to_datetime(df["open_date"])
    today = pd.timestamp.today().normalize()
    invalid_dates = df[(transaction_date < open_date) | (transaction_date > today)]
    if not invalid_dates.empty():
        raise ValueError(
            "\n".join(
                [
                    "Invalid dates found for columns: \n"
                    f"{row.transaction_id},{row.account_id},"
                    f"{row.open_date},{row.transaction_date}"
                    for row in invalid_dates.itertuples()
                ]
            )
        )
    return True


def check_foreign_keys(
    child_df: pd.DataFrame,
    parent_df: pd.DataFrame,
    child_column: str,
    parent_column: str,
) -> bool:
    valid_mask = child_df[child_column].isin(parent_df[parent_column])
    invalid_foreign_keys = child_df.loc[~valid_mask, child_column].unique()
    invalid_foreign_keys = sorted(invalid_foreign_keys)

    if invalid_foreign_keys:
        raise ValueError(f"Invalid {child_column} values found: {invalid_foreign_keys}")
    return True


def validate(customers_df, accounts_df, transactions_df):
    check_duplicates(customers_df, "customer_id")
    check_duplicates(accounts_df, "account_id")
    check_duplicates(transactions_df, "transaction_id")

    check_missing_values(
        customers_df,
        ["customer_id", "full_name", "province", "date_of_birth"],
    )

    check_missing_values(
        accounts_df,
        ["account_id", "customer_id", "account_type", "open_date", "balance"],
    )

    check_missing_values(
        transactions_df,
        [
            "transaction_id",
            "account_id",
            "transaction_date",
            "transaction_type",
            "amount",
            "transaction_channel",
        ],
    )

    check_allowed_types(
        accounts_df,
        "account_type",
        ["Savings", "Cheque", "Credit", "Business"],
    )

    check_allowed_types(
        transactions_df,
        "transactions_type",
        ["Deposit", "Withdrawal", "Card Purchase", "Salary", "EFT"],
    )

    check_allowed_types(
        transactions_df,
        "merchant_name",
        ["ATM", "Mobile App", "Online Banking", "Branch", "POS"],
    )

    check_allowed_types(
        customers_df,
        "province",
        [
            "Gauteng",
            "Western Cape",
            "KwaZulu-Natal",
            "Limpopo",
            "Mpumalanga",
            "North West",
            "Northern Cape",
            "Eastern Cape",
            "Free State",
        ],
    )

    check_foreign_keys(accounts_df, customers_df, "customer_id", "customer_id")

    check_foreign_keys(transactions_df, accounts_df, "transaction_id", "transaction_id")

    check_transaction_amounts(transactions_df, "amount")

    check_transaction_dates(transactions_df, accounts_df)

    print("Validation passed.")


if __name__ == "__main__":
    validate(customers_df, accounts_df, transactions_df)
