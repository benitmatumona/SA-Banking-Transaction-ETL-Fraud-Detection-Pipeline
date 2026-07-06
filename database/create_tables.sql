CREATE TABLE customers(
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(100),
    province VARCHAR(100),
    join_date date
);

CREATE TABLE accounts(
    account_id INT PRIMARY KEY,
    customer_id INT,
    account_type VARCHAR(100),
    open_date DATE,

    CONSTRAINT fk_accounts_customers 
        FOREIGN KEY customer_id 
        REFERENCES customers.customer_id
);

CREATE TABLE transactions(
    transaction_id INT PRIMARY KEY,
    account_id INT ,
    transaction_date DATE,
    transaction_type VARCHAR(100),
    merchant_name VARCHAR(100),
    amount INT,
    reference VARCHAR(100)
    balance_after_transaction INT,
    if_fraud BOOLEAN,

    CONSTRAINT fk_transactions_accounts 
        FOREIGN KEY account_id 
        REFERENCES accounts.account_id
);