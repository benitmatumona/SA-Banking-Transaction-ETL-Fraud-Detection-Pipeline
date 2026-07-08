import pandas as pd

customers_df = pd.read_csv(...)
accounts_df = pd.read_csv(...)
transactions_df = pd.read_csv()


def check_duplicates(df: pd.DataFrame, column_name: str) -> bool:
    if df[column_name].duplicated().any():
        raise ValueError(
            f"Duplicate values found in '{column_name}'."
        )
    return True


def check_missing_values(
    df: pd.DataFrame,
    required_columns: list[str]
) -> bool:
    
    for column in required_columns:
        if df[column].isnull().any():
            raise ValueError(
                f"Missing values found in '{column}'."
            )
    return True
            


def check_primary_keys():
    pass


def check_allowed_types(
    df: pd.DataFrame,
    column_name: str,
    allowed_types: list[str]    
)-> bool:
    valid_mask: list[bool] = df[column_name].isin(allowed_types)
    invalid_values = set()

    for value, is_valid in zip(df[column_name], valid_mask):
        if not is_valid:
            invalid_values.add(value)
    if invalid_values:
        raise ValueError(
            f"Invalid {column_name} found '{sorted(invalid_values)}'."
        )
    return True    


def check_provinces():
    pass


def check_transaction_amounts(
    df: pd.DataFrame
)-> bool:
    Max_TRANSACTION_AMOUNT = 10_000_000

    if (df["amount"].isna()).any():
        raise ValueError(
            f"Missing values found in the column 'amount'."
        )
    if (df["amount"] <= 0).any():
        raise ValueError(
            "Transaction amounts must be greater than 0."
        ) 
    if (df["amount"] > Max_TRANSACTION_AMOUNT).any():
        raise ValueError(
            "Transaction amounts cannot be greater than 10 000 000."
        )
    return True


def check_transaction_dates():
    pass


def check_foreign_keys(
    child_df: pd.DataFrame,
    parent_df: pd.DataFrame,
    child_column: str,
    parent_column: str 
)-> bool:
    valid_mask = child_df[child_column].isin(parent_df[parent_column])
    invalid_foreign_keys = sorted(
        child_column.loc[~valid_mask, child_column].unique()
    )

    if invalid_foreign_keys:
        raise ValueError(
            f"Invalid {child_column} values found: "
            f"{sorted(invalid_foreign_keys)}"
        )
    return True


def validate():
    check_duplicates()
    check_missing_values()
    check_primary_keys()
    check_allowed_types()
    check_provinces()
    check_transaction_amounts()
    check_transaction_dates()
    check_foreign_keys()

    print("Validation passed.")


if __name__ == "__main__":
    validate()