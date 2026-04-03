from typing import List


def recommend_actions(
    churn_probability: float,
    risk_segment: str,
    top_risk_drivers: list[dict],
    customer_data: dict | None = None
) -> List[str]:
    recommendations = []

    customer_data = customer_data or {}
    driver_names = [d["feature"] for d in top_risk_drivers]

    if risk_segment == "Low":
        return ["No immediate retention action needed. Monitor customer normally."]

    if risk_segment == "Medium":
        recommendations.append("Schedule a light-touch retention check-in.")

    if risk_segment == "High":
        recommendations.append("Prioritize this customer for retention outreach.")

    if any("contract_type = Month-to-month" in d for d in driver_names):
        recommendations.append("Offer a discount for switching to a longer-term contract.")

    if any("payment_method = Electronic check" in d for d in driver_names):
        recommendations.append("Encourage switching to a more stable payment method such as automatic card payment.")

    if any("monthly_charges" in d for d in driver_names):
        recommendations.append("Review pricing and offer a loyalty discount or better-value bundle.")

    if any("tenure_months" in d for d in driver_names):
        tenure = customer_data.get("tenure_months")
        if tenure is not None and tenure < 12:
            recommendations.append("Launch an onboarding or early-lifecycle retention campaign for newer customers.")

    if customer_data.get("has_internet") == 1 and customer_data.get("num_services", 0) <= 2:
        recommendations.append("Promote additional bundled services to increase stickiness and perceived value.")

    if customer_data.get("dependents") == 0 and risk_segment == "High":
        recommendations.append("Test a personalized offer tailored to individual usage and value perception.")

    if churn_probability >= 0.8:
        recommendations.append("Escalate to a high-priority retention workflow immediately.")

    # Remove duplicates while preserving order
    unique_recommendations = list(dict.fromkeys(recommendations))

    if not unique_recommendations:
        unique_recommendations.append("Review customer account manually for a tailored retention action.")

    return unique_recommendations