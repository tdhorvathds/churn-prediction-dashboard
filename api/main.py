from fastapi import FastAPI
from api.schemas import CustomerInput, PredictionResponse
from src.predict import predict_single

app = FastAPI(
    title="Customer Churn Prediction API",
    description="FastAPI service for churn prediction and later explainability.",
    version="0.1.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerInput):
    result = predict_single(customer.model_dump())
    return result