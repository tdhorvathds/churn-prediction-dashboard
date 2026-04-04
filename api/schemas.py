from pydantic import BaseModel, Field


class CustomerInput(BaseModel):
    customer_id: str | None = Field(default=None, description="Optional customer identifier")
    senior_citizen: int = Field(..., description="1 if the customer is a senior citizen, else 0")
    partner: int = Field(..., description="1 if the customer has a partner, else 0")
    dependents: int = Field(..., description="1 if the customer has dependents, else 0")
    tenure_months: float = Field(..., description="Customer tenure in months")
    monthly_charges: float = Field(..., description="Monthly subscription charges")
    total_charges: float = Field(..., description="Total charges billed to the customer")
    phone_service: int = Field(..., description="1 if the customer has phone service")
    multiple_lines: int = Field(..., description="1 if the customer has multiple lines")
    online_security: int = Field(..., description="1 if the customer has online security")
    online_backup: int = Field(..., description="1 if the customer has online backup")
    device_protection: int = Field(..., description="1 if the customer has device protection")
    tech_support: int = Field(..., description="1 if the customer has tech support")
    streaming_tv: int = Field(..., description="1 if the customer has tv streaming")
    streaming_movies: int = Field(..., description="1 if the customer has movie streaming")
    gender: str = Field(..., description="Customer gender")
    city: str = Field(..., description="Customer city")
    contract_type: str = Field(..., description="Contract type")
    payment_method: str = Field(..., description="Payment method")
    internet_service: str = Field(..., description="Internet service type")

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
                "phone_service": 1,
                "multiple_lines": 1,
                "online_security": 0,
                "online_backup": 0,
                "device_protection": 1,
                "tech_support": 0,
                "streaming_tv": 1,
                "streaming_movies": 1,
                "gender": "Female",
                "city": "Los Angeles",
                "contract_type": "Month-to-month",
                "payment_method": "Electronic check",
                "internet_service": "DSL"
            }
        }
    }


class RecommendationItem(BaseModel):
    priority: str
    category: str
    action: str


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
    customer_id: str | None = Field(..., description="Customer identifier")
    churn_probability: float = Field(..., description="Predicted probability of churn")
    top_risk_drivers: list[FeatureImpact] = Field(..., description="Top features increasing churn risk")
    top_protective_drivers: list[FeatureImpact] = Field(..., description="Top features decreasing churn risk")
    recommended_actions: list[RecommendationItem] = Field(..., description="Recommended retention actions")