CREATE DATABASE IF NOT EXISTS churn_db;
USE churn_db;

DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS churn;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers(
	customer_id VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(20),
    senior_citizen BOOLEAN,
    partner BOOLEAN,
    dependents BOOLEAN,
    tenure_months INT,
    country VARCHAR(50),
    state VARCHAR(50),
    city VARCHAR(100),
    zip_code VARCHAR(20),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6)
);

CREATE TABLE services (
    customer_id VARCHAR(20) PRIMARY KEY,
    phone_service BOOLEAN,
    multiple_lines VARCHAR(20),
    internet_service VARCHAR(50),
    online_security VARCHAR(20),
    online_backup VARCHAR(20),
    device_protection VARCHAR(20),
    tech_support VARCHAR(20),
    streaming_tv VARCHAR(20),
    streaming_movies VARCHAR(20),
    contract_type VARCHAR(50),
    paperless_billing BOOLEAN,
    payment_method VARCHAR(100),
    monthly_charges DECIMAL(10,2),
    total_charges DECIMAL(10,2),
    CONSTRAINT fk_services_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE churn (
    customer_id VARCHAR(20) PRIMARY KEY,
    churn_label BOOLEAN,
    churn_value INT,
    churn_score INT,
    cltv DECIMAL(10,2),
    churn_reason VARCHAR(255),
    CONSTRAINT fk_churn_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE predictions (
    customer_id VARCHAR(20) PRIMARY KEY,
    churn_probability DECIMAL(5,4),
    risk_segment VARCHAR(20),
    estimated_revenue_at_risk DECIMAL(10,2),
    predicted_on DATE,
    model_name VARCHAR(100),
    CONSTRAINT fk_predictions_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
        
