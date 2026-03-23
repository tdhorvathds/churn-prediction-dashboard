# Customer Churn Prediction & Revenue Impact Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![ML](https://img.shields.io/badge/Machine%20Learning-XGBoost-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

End-to-end data science project combining **SQL, Python, and Power BI** to identify customers at risk of churn and quantify the associated revenue impact. The solution integrates data modeling, machine learning, and business intelligence to support data-driven retention strategies.

---

## Business Problem

Customer churn is a major challenge for subscription-based businesses. Losing customers not only reduces revenue but also increases acquisition costs.

The goal of this project is to:

- Predict customer churn
- Segment customers by risk level
- Quantify **revenue at risk**
- Support **data-driven retention strategies**
- Provide actionable insights through an **interactive dashboard**

---

## Solution Overview

This project follows a full data pipeline:

- Structured customer data stored in **MySQL**
- Data cleaning and feature engineering using **Python**
- Churn prediction using **XGBoost**
- Risk segmentation (High / Medium / Low)
- Calculation of estimated revenue at risk
- Interactive **Power BI dashboard** for business users 

---

## Dashboard Preview

**Overview**

- Churn rate and revenue impact
- Key KPIs and high-risk customers

![Overview](dashboard/screenshots/overview.png)

**Churn Drivers**

- Analysis of factors influencing churn:
- Payment method
- Internet service
- Technical support & online security
- Customer lifetime value (CLTV)

![Drivers](dashboard/screenshots/drivers.png)

**Risk Segmentation & Geography**

- Identification of high-risk regions
- Top cities by revenue at risk
- Interactive map visualization

![Map](dashboard/screenshots/map.png)

![Map](dashboard/screenshots/map_filter.png)

---

## Key Insights

- ~30% of monthly revenue is at risk
- Month-to-month customers show the highest churn rates
- Customers without technical support or online security are significantly more likely to churn
- Fiber optic users exhibit higher churn risk compared to DSL users
- Revenue risk is concentrated in major urban areas such as Los Angeles

---

## Tech Stack

- **Python** (pandas, scikit-learn, XGBoost)
- **MySQL**
- **Power BI**
- **Jupyter Notebook**

---

## Data Pipeline

- Raw data is cleaned and preprocessed in **Python**
- Structured tables are created in **MySQL**
- SQL queries are used for feature preparation
- Machine learning model predicts churn probability
- Predictions are stored and enriched with business metrics
- **Power BI** connects to the database for visualization

---

## Machine Learning

- Model: **XGBoost classifier**
- Target: Customer churn (binary classification)

### Techniques:

- Handling class imbalance
- Feature engineering
- Hyperparameter tuning

### Outputs:

- Churn probability
- Risk segmentation
- Estimated revenue at risk

## How To Run

1. Set up MySQL database using:

`schema.sql`

`tables/*.sql`

2. Load and preprocess data using Jupyter notebooks:

`01_data_cleaning.ipynb`

3. Train model:

`03_model_training.ipynb`

4. Export predictions to database or CSV

5. Open Power BI dashboard:

`dashboard/churn_dashboard.pbix`

---

### Business Value

This project demonstrates how data science can be used to:

- Identify high-risk customers
- Prioritize retention efforts
- Quantify financial impact
- Support data-driven decision-making

---

### Future Improvements

- Model deployment (API or batch pipeline)
- Real-time prediction integration
- A/B testing for retention strategies
- Advanced customer segmentation

### Author

Built by [Tamas David Horvath](https://github.com/tdhorvathds)

Let's connect on [LinkedIn](https://www.linkedin.com/in/tdhorvathds/)
