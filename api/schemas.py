from pydantic import BaseModel


class CustomerInput(BaseModel):
    customer_id: str | None = None
    senior_citizen: int
    partner: int
    dependents: int
    tenure_months: float
    monthly_charges: float
    total_charges: float
    has_internet: int
    num_services: int
    churn_score: float
    cltv: float
    gender: str
    city: str
    contract_type: str
    payment_method: str


class PredictionResponse(BaseModel):
    customer_id: str | None = None
    churn_probability: float
    risk_segment: str
    estimated_revenue_at_risk: float
    model_name: str


class FeatureImpact(BaseModel):
    feature: str
    shap_value: float


class ExplanationResponse(BaseModel):
    customer_id: str
    churn_probability: float
    top_risk_drivers: list[FeatureImpact]
    top_protective_drivers: list[FeatureImpact]