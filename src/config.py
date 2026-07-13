VALID_PROVINCES = [
    "Gauteng",
    "Western Cape",
    "KwaZulu-Natal",
    "Limpopo",
    "Mpumalanga",
    "North West",
    "Free State",
    "Northern Cape",
    "Eastern Cape",
]

ACCOUNT_TYPES = ["Cheque", "Savings", "Credit", "Business"]

TRANSACTION_CHANNELS = [
    "ATM",
    "POS",
    "Online",
    "Mobile App",
    "Branch",
    "Online Banking",
]

TRANSACTION_TYPES = {
    "Deposit": "CASH DEPOSIT",
    "Withdrawal": "ATM CASH WITHDRAWAL",
    "Card Purchase": "merchant_name",
    "EFT": "EFT TO merchant_name",
    "Salary": "MONTHLY SALARY",
}
