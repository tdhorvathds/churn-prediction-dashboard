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
    API for predicting customer churn risk and explaining the key drivers behind each prediction.

    Features:
    - predict churn from manual input
    - predict churn directly from database by customer_id
    - explain top churn risk and protective drivers with SHAP
    """,
    version="0.2.0",
)


@app.get("/health",
        tags=["System"],
        summary="Health check",
        description="Simple endpoint to verify that the API is running.")
def health():
    return {"status": "ok"}


@app.post("/predict",
        response_model=PredictionResponse,
        tags=["Prediction"],
        summary="Predict churn from manual input",
        description="Score a single customer from a JSON payload and return churn probability, risk segment, and estimated revenue at risk.")
def predict(customer: CustomerInput):
    result = predict_single(customer.model_dump())
    return result


@app.get("/predict-by-id/{customer_id}",
        response_model=PredictionResponse,
        tags=["Prediction"],
        summary="Predict churn by customer ID",
        description="Fetch a customer from the database by customer_id and return the churn prediction.")
def predict_by_id(customer_id: str):
    try:
        return predict_single_by_id(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/explain-by-id/{customer_id}", 
        response_model=ExplanationResponse,
        tags=["Explainability"],
        summary="Explain churn prediction by customer ID",
        description="Return the top SHAP-based risk and protective drivers for a customer fetched from the database.")
def explain_by_id(customer_id: str):
    try:
        return explain_single_customer_summary(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@app.post(
    "/explain",
    response_model=ExplanationResponse,
    tags=["Explainability"],
    summary="Explain churn prediction from manual input",
    description="Score a manually provided customer payload and return the top SHAP-based churn drivers."
)
def explain(customer: CustomerInput):
    return explain_customer_payload(customer.model_dump())