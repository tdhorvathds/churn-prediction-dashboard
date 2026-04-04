CREATE DATABASE IF NOT EXISTS churn_project;
USE churn_project;
        
CREATE VIEW model_features AS
SELECT
    c.customer_id,
    c.gender,
    c.senior_citizen,
    c.partner,
    c.dependents,
    c.tenure_months,
    c.city,
    s.contract_type,
    s.payment_method,
    s.monthly_charges,
    s.total_charges,
	s.phone_service,
    s.multiple_lines,
	s.internet_service,
	s.online_security,
	s.online_backup,
	s.device_protection,
	s.tech_support,
	s.streaming_tv,
	s.streaming_movies,
    ch.churn_value,
    ch.churn_score,
    ch.cltv
FROM customers c
JOIN services s ON c.customer_id = s.customer_id
JOIN churn ch ON c.customer_id = ch.customer_id;
