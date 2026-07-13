CREATE TABLE customers(
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    join_date date NOT NULL
);

CREATE TABLE accounts(
    account_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_type VARCHAR(100) NOT NULL,
    open_date DATE NOT NULL,

    CONSTRAINT fk_accounts_customers 
        FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id)
);

CREATE TABLE transactions(
    transaction_id INT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(100) NOT NULL,
    transaction_channel VARCHAR(50) NOT NULL,
    merchant_name VARCHAR(100),
    amount NUMERIC(12,2) NOT NULL,
    reference VARCHAR(100) NOT NULL,
    balance_after_transaction INT NOT NULL,
    is_fraud BOOLEAN,

    CONSTRAINT fk_transactions_accounts 
        FOREIGN KEY (account_id) 
        REFERENCES accounts(account_id)
);