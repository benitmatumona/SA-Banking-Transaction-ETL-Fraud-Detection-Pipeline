import pandas as pd

customers_df = pd.read_csv(...)
accounts_df = pd.read_csv(...)
transactions_df = pd.read_csv()


def check_duplicates(df: pd.DataFrame, column_name: str) -> bool:
    if df[column_name].duplicated().any():
        raise ValueError(f"Duplicate values found in '{column_name}'.")
    return True


def check_missing_values(
    df: pd.DataFrame,
    required_columns: list[str]
) -> bool:
    
    for column in required_columns:
        if df[column].isnull().any():
            raise ValueError(f"Missing values found in '{column}'.")
    return True
            


def check_primary_keys():
    pass


def check_account_types(
    df: pd.DataFrame,
    valid_account_types: list[str]    
)-> bool:
    ...
    



def check_provinces():
    pass


def check_transaction_amounts():
    pass


def check_transaction_dates():
    pass


def check_customer_foreign_keys():
    pass


def check_account_foreign_keys():
    pass


def validate():
    check_duplicates()
    check_missing_values()
    check_primary_keys()
    check_account_types()
    check_provinces()
    check_transaction_amounts()
    check_transaction_dates()
    check_customer_foreign_keys()
    check_account_foreign_keys()

    print("Validation passed.")


if __name__ == "__main__":
    validate()