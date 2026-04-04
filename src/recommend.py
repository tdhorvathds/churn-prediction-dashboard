from typing import List, Dict


def recommend_actions(
    churn_probability: float,
    risk_segment: str,
    top_risk_drivers: list[dict],
    customer_data: dict | None = None
) -> List[Dict[str, str]]:
    recommendations = []

    customer_data = customer_data or {}
    driver_names = [d["feature"] for d in top_risk_drivers]

    contract_type = customer_data.get("contract_type")
    payment_method = customer_data.get("payment_method")
    internet_service = customer_data.get("internet_service")
    tenure = customer_data.get("tenure_months")

    def add_recommendation(priority: str, category: str, action: str):
        recommendations.append(
            {
                "priority": priority,
                "category": category,
                "action": action
            }
        )

    if risk_segment == "Low":
        return [
            {
                "priority": "Low",
                "category": "Monitoring",
                "action": "No immediate retention action needed. Monitor customer normally."
            }
        ]

    if risk_segment == "Medium":
        add_recommendation(
            "Medium",
            "Outreach",
            "Schedule a light-touch retention check-in."
        )

    if risk_segment == "High":
        add_recommendation(
            "High",
            "Outreach",
            "Prioritize this customer for retention outreach."
        )

    if churn_probability >= 0.8:
        add_recommendation(
            "High",
            "Escalation",
            "Escalate to a high-priority retention workflow immediately."
        )

    if "contract_type" in driver_names and contract_type == "Month-to-month":
        add_recommendation(
            "High",
            "Contract",
            "Offer a discount for switching to a longer-term contract."
        )

    if "payment_method" in driver_names and payment_method == "Electronic check":
        add_recommendation(
            "Medium",
            "Payment",
            "Encourage switching to a more stable payment method such as automatic card payment."
        )

    if "monthly_charges" in driver_names:
        add_recommendation(
            "Medium",
            "Pricing",
            "Review pricing and offer a loyalty discount or better-value bundle."
        )

    if "tenure_months" in driver_names and tenure is not None and tenure < 12:
        add_recommendation(
            "Medium",
            "Lifecycle",
            "Launch an onboarding or early-lifecycle retention campaign for newer customers."
        )

    if "tech_support" in driver_names and customer_data.get("tech_support") == 0:
        add_recommendation(
            "Medium",
            "Support",
            "Offer a free technical support trial or discounted support add-on."
        )

    if "online_security" in driver_names and customer_data.get("online_security") == 0:
        add_recommendation(
            "Medium",
            "Security",
            "Promote an online security add-on to increase perceived value and stickiness."
        )

    if "online_backup" in driver_names and customer_data.get("online_backup") == 0:
        add_recommendation(
            "Low",
            "Bundle",
            "Recommend an online backup add-on as part of a retention bundle."
        )

    if "device_protection" in driver_names and customer_data.get("device_protection") == 0:
        add_recommendation(
            "Low",
            "Bundle",
            "Offer device protection as part of a loyalty or bundle package."
        )

    if "internet_service" in driver_names and internet_service == "Fiber optic":
        add_recommendation(
            "Medium",
            "Service Quality",
            "Review service quality and pricing for fiber optic customers in this segment."
        )

    if (
        customer_data.get("phone_service") == 1
        and customer_data.get("multiple_lines") == 0
        and risk_segment in ["Medium", "High"]
    ):
        add_recommendation(
            "Low",
            "Bundle",
            "Promote a multiple-lines bundle to improve account stickiness."
        )

    service_flags = [
        customer_data.get("phone_service", 0),
        customer_data.get("multiple_lines", 0),
        customer_data.get("online_security", 0),
        customer_data.get("online_backup", 0),
        customer_data.get("device_protection", 0),
        customer_data.get("tech_support", 0),
        customer_data.get("streaming_tv", 0),
        customer_data.get("streaming_movies", 0),
    ]
    active_services = sum(int(bool(x)) for x in service_flags)

    if active_services <= 2 and risk_segment in ["Medium", "High"]:
        add_recommendation(
            "Medium",
            "Bundle",
            "Promote bundled services to increase customer stickiness and perceived value."
        )

    if customer_data.get("dependents") == 0 and risk_segment == "High":
        add_recommendation(
            "Low",
            "Personalization",
            "Test a personalized offer tailored to individual usage and value perception."
        )

    if "city" in driver_names:
        add_recommendation(
            "Low",
            "Regional Analysis",
            "Review whether location-specific pricing, service quality, or competition may be influencing churn risk."
        )

    # remove duplicates while preserving order
    seen = set()
    unique_recommendations = []

    for rec in recommendations:
        key = (rec["priority"], rec["category"], rec["action"])
        if key not in seen:
            seen.add(key)
            unique_recommendations.append(rec)

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }

    unique_recommendations = sorted(
        unique_recommendations,
        key=lambda x: priority_order.get(x["priority"], 99)
    )

    if not unique_recommendations:
        unique_recommendations.append(
            {
                "priority": "Medium",
                "category": "Review",
                "action": "Review customer account manually for a tailored retention action."
            }
        )

    return unique_recommendations