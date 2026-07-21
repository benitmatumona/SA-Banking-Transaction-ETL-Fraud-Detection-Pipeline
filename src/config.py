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

TRANSACTION_CHANNELS = {
    "Deposit": ["ATM", "Branch"],
    "Withdrawal": ["ATM", "Branch"],
    "Card Purchase": ["POS", "Online"],
    "Salary": ["Online Banking"],
    "EFT": ["Online Banking", "Mobile App"],
}

TRANSACTION_TYPES = {
    "Deposit": "CASH DEPOSIT",
    "Withdrawal": "ATM CASH WITHDRAWAL",
    "Card Purchase": "merchant_name",
    "EFT": "EFT TO merchant_name",
    "Salary": "MONTHLY SALARY",
}

ALL_TRANSACTION_CHANNELS = sorted(
    {
        channel 
        for channels in TRANSACTION_CHANNELS.values()
        for channel in channels
    }
)


MERCHANTS = {
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

MAX_TRANSACTION_AMOUNT = 10_000_000


DB_USER = "postgres"
DB_PASSWORD = ""
DB_NAME = "south_africa_bank"
