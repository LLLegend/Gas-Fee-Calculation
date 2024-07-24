CREATE DATABASE IF NOT EXISTS test_db;

USE test_db;

CREATE TABLE IF NOT EXISTS transactions (
    block_number int,
    transaction_hash VARCHAR(255),
    gas_price BIGINT,
    gas_used BIGINT,
    transaction_timestamp int
);

CREATE TABLE IF NOT EXISTS prices (
    price_date datetime,
    price float
);


