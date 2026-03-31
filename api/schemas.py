from pydantic import BaseModel, Field


class CustomerInput(BaseModel):
    customer_id: str | None = Field(default=None, description="Optional customer identifier")
    senior_citizen: int = Field(..., description="1 if the customer is a senior citizen, else 0")
    partner: int = Field(..., description="1 if the customer has a partner, else 0")
    dependents: int = Field(..., description="1 if the customer has dependents, else 0")
    tenure_months: float = Field(..., description="Customer tenure in months")
    monthly_charges: float = Field(..., description="Monthly subscription charges")
    total_charges: float = Field(..., description="Total charges billed to the customer")
    has_internet: int = Field(..., description="1 if the customer has internet service, else 0")
    num_services: int = Field(..., description="Number of subscribed services")
    churn_score: float = Field(..., description="Internal churn score feature")
    cltv: float = Field(..., description="Customer lifetime value")
    gender: str = Field(..., description="Customer gender")
    city: str = Field(..., description="Customer city")
    contract_type: str = Field(..., description="Contract type")
    payment_method: str = Field(..., description="Payment method")

    model_config = {
        "json_schema_extra": {
            "example": {
                "customer_id": "7590-VHVEG",
                "senior_citizen": 0,
                "partner": 1,
                "dependents": 0,
                "tenure_months": 12,
                "monthly_charges": 75.5,
                "total_charges": 906.0,
                "has_internet": 1,
                "num_services": 3,
                "churn_score": 45,
                "cltv": 3200,
                "gender": "Female",
                "city": "Los Angeles",
                "contract_type": "Month-to-month",
                "payment_method": "Electronic check"
            }
        }
    }


class PredictionResponse(BaseModel):
    customer_id: str | None = Field(default=None, description="Customer identifier")
    churn_probability: float = Field(..., description="Predicted probability of churn")
    risk_segment: str = Field(..., description="Risk segment: Low, Medium, or High")
    estimated_revenue_at_risk: float = Field(..., description="Monthly revenue weighted by churn probability")
    model_name: str = Field(..., description="Name of the prediction model")


class FeatureImpact(BaseModel):
    feature: str = Field(..., description="Feature name in business-friendly format")
    shap_value: float = Field(..., description="SHAP contribution value")


class ExplanationResponse(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    churn_probability: float = Field(..., description="Predicted probability of churn")
    top_risk_drivers: list[FeatureImpact] = Field(..., description="Top features increasing churn risk")
    top_protective_drivers: list[FeatureImpact] = Field(..., description="Top features decreasing churn risk")