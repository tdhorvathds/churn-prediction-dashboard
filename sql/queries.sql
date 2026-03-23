USE churn_db;

-- Churn rate by contract type

SELECT 
    s.contract_type,
    COUNT(*) AS total_customers,
    SUM(ch.churn_value) AS churned_customers,
    ROUND(100.0 * SUM(ch.churn_value) / COUNT(*), 2) AS churn_rate_pct
FROM services s
JOIN churn ch ON s.customer_id = ch.customer_id
GROUP BY s.contract_type
ORDER BY churn_rate_pct DESC;

-- Monthly revenue at risk by churned customers

SELECT 
    ROUND(SUM(s.monthly_charges), 2) AS monthly_revenue_at_risk
FROM services s
JOIN churn ch ON s.customer_id = ch.customer_id
WHERE ch.churn_value = 1;

-- Top churn reasons

SELECT 
    churn_reason,
    COUNT(*) AS cnt
FROM churn
WHERE churn_value = 1
GROUP BY churn_reason
ORDER BY cnt DESC
LIMIT 10;

-- Churn rate by payment method

SELECT s.payment_method,
COUNT(*) AS total_customers,
SUM(ch.churn_value) AS churned_customers,
ROUND(100 * SUM(ch.churn_value) / COUNT(*), 2) AS churn_rate_pct
FROM services s
JOIN churn ch ON s.customer_id = ch.customer_id
GROUP BY s.payment_method
ORDER BY churn_rate_pct DESC;

-- Average monthly charges: churned vs retained

SELECT ROUND(AVG(s.total_charges), 2) AS avg_total_charges,
ROUND(AVG(s.monthly_charges), 2) AS avg_monthly_charges,
COUNT(*) AS total_customers,
ch.churn_value
FROM services s
JOIN churn ch ON s.customer_id = ch.customer_id
GROUP BY ch.churn_value;

-- Churn by tenure bucket

SELECT
    CASE
        WHEN c.tenure_months <= 12 THEN '0-12 months'
        WHEN c.tenure_months <= 24 THEN '13-24 months'
        WHEN c.tenure_months <= 48 THEN '25-48 months'
        ELSE '49+ months'
    END AS tenure_group,
    COUNT(*) AS total_customers,
    SUM(ch.churn_value) AS churned_customers,
    ROUND(100 * SUM(ch.churn_value) / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN churn ch ON c.customer_id = ch.customer_id
GROUP BY tenure_group
ORDER BY churn_rate_pct DESC;

-- Churn by internet service type

SELECT s.internet_service,
COUNT(*) AS total_customers,
SUM(ch.churn_value) AS churned_customers
FROM churn ch
JOIN services s ON s.customer_id = ch.customer_id
GROUP BY s.internet_service;

-- Customers with highest CLTV among churned customers

SELECT ch.customer_id,
ch.cltv
FROM churn ch
WHERE ch.churn_value = 1
ORDER BY ch.cltv DESC
LIMIT 10;

-- Revenue at risk by contract type

SELECT s.contract_type,
ROUND(SUM(CASE WHEN ch.churn_value = 1 THEN s.monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_risk,
SUM(ch.churn_value) AS churned_customers
FROM services s
JOIN churn ch ON s.customer_id = ch.customer_id
GROUP BY s.contract_type
ORDER BY monthly_revenue_at_risk DESC;

-- Top city-level churn hotspots

SELECT c.city,
SUM(ch.churn_value) AS churned_customers
FROM customers c
JOIN churn ch ON c.customer_id = ch.customer_id
GROUP BY c.city
ORDER BY churned_customers DESC
LIMIT 10;

SELECT
    c.city,
    COUNT(*) AS total_customers,
    SUM(ch.churn_value) AS churned_customers,
    ROUND(100 * SUM(ch.churn_value) / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN churn ch ON c.customer_id = ch.customer_id
GROUP BY c.city
HAVING COUNT(*) >= 30
ORDER BY churn_rate_pct DESC, total_customers DESC
LIMIT 15;

-- Service count per customer and churn

SELECT
    c.customer_id,
    (
        s.phone_service +
        s.multiple_lines +
        (s.internet_service <> 'No') +
        s.online_security +
        s.online_backup +
        s.device_protection+
        s.tech_support +
        s.streaming_tv +
        s.streaming_movies
    ) AS num_services,
    ch.churn_value
FROM customers c
JOIN services s ON c.customer_id = s.customer_id
JOIN churn ch ON c.customer_id = ch.customer_id
LIMIT 20;