from fastapi import FastAPI, HTTPException
from api.schemas import (
    CustomerInput,
    PredictionResponse,
    ExplanationResponse,
)
from src.predict import predict_single, predict_single_by_id
from src.explain import explain_single_customer_summary


app = FastAPI(
    title="Customer Churn Prediction API",
    description="FastAPI service for churn prediction and SHAP explanations.",
    version="0.1.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerInput):
    result = predict_single(customer.model_dump())
    return result


@app.get("/predict-by-id/{customer_id}", response_model=PredictionResponse)
def predict_by_id(customer_id: str):
    try:
        return predict_single_by_id(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/explain-by-id/{customer_id}", response_model=ExplanationResponse)
def explain_by_id(customer_id: str):
    try:
        return explain_single_customer_summary(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))