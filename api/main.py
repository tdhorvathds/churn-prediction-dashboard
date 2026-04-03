from fastapi import FastAPI, HTTPException
from api.schemas import (
    CustomerInput,
    PredictionResponse,
    ExplanationResponse,
)
from src.predict import predict_single, predict_single_by_id
from src.explain import explain_single_customer_summary, explain_customer_payload


app = FastAPI(
    title="Customer Churn Prediction API",
    description="""
    API for predicting customer churn risk, identifying key churn drivers and generating retention recommendations.

    Features:
    - Predict churn probability for a customer
    - Return churn risk segment (Low / Medium / High)
    - Explain predictions using SHAP values
    - Generate customer-specific retention recommendations
    - Retrieve explanations for existing customer IDs
    """,
    version="1.0.0",
    contact={
        "name": "Tamas David Horvath",
        "url": "https://github.com/tdhorvathds",
    },
)


@app.get(
    "/health",
    tags=["Health Check"],
    summary="API status check",
    description="Simple endpoint to verify that the API is running successfully."
)
def root():
    return {
        "message": "Customer Churn Prediction API is running."
    }


@app.post("/predict",
        response_model=PredictionResponse,
        tags=["Prediction"],
        summary="Predict churn from manual input",
        description="""
        Predicts the probability that a customer will churn based on their profile,
        contract details, service usage, and billing information.

        Returns:
        - churn probability
        - churn risk segment
        - estimated revenue at risk
        """
)
def predict(customer: CustomerInput):
    result = predict_single(customer.model_dump())
    return result


@app.get("/predict-by-id/{customer_id}",
        response_model=PredictionResponse,
        tags=["Prediction"],
        summary="Predict churn for an existing customer",
        description="""
        Retrieves a customer record from the dataset using the provided customer ID
        and returns a churn prediction.

        Returns:
        - churn probability
        - churn risk segment
        - estimated revenue at risk

        """
    )
def predict_by_id(customer_id: str):
    try:
        return predict_single_by_id(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@app.post(
    "/explain",
    response_model=ExplanationResponse,
    tags=["Explainability"],
    summary="Explain churn prediction from manual input",
    description="""
    Generates a churn prediction explanation for a customer payload.

    Returns:
    - churn probability
    - top risk drivers
    - top protective drivers
    - recommended retention actions

    SHAP values are used to explain which features increase or decrease churn risk.
    """
)
def explain(customer: CustomerInput):
    return explain_customer_payload(customer.model_dump())


@app.get("/explain-by-id/{customer_id}", 
        response_model=ExplanationResponse,
        tags=["Explainability"],
        summary="Explain churn prediction by customer ID",
        description="""
        Retrieves churn explanation details for an existing customer ID from the dataset.

        Returns:
        - churn probability
        - top churn drivers
        - top protective factors
        - recommended retention actions

        Useful for customer success teams reviewing specific accounts.
        """
)
def explain_by_id(customer_id: str):
    try:
        return explain_single_customer_summary(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    