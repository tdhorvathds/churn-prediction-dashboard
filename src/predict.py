import pandas as pd

from src.config import PREDICTIONS_DIR, TIMESTAMP
from src.data_loader import load_model_features, get_engine, load_customer_by_id
from src.preprocessing import FEATURE_COLS
from src.utils import load_pipeline


def risk_segment(probability: float) -> str:
    if probability > 0.7:
        return "High"
    elif probability > 0.4:
        return "Medium"
    else:
        return "Low"

def generate_predictions(df: pd.DataFrame) -> pd.DataFrame:
    pipeline = load_pipeline()

    X = df[FEATURE_COLS].copy()
    churn_probabilities = pipeline.predict_proba(X)[:, 1]

    predictions = df.copy()
    predictions["churn_probability"] = churn_probabilities
    predictions["predicted_on"] = pd.Timestamp.now()
    predictions["risk_segment"] = predictions["churn_probability"].apply(risk_segment)
    predictions["estimated_revenue_at_risk"] = (
        predictions["monthly_charges"] * predictions["churn_probability"]
    )
    predictions["model_name"] = "XGBoost"

    return predictions[
        [
            "customer_id",
            "churn_probability",
            "risk_segment",
            "estimated_revenue_at_risk",
            "predicted_on",
            "model_name",
        ]
    ].copy()

def predict_single(customer_data: dict) -> dict:
    pipeline = load_pipeline()

    input_df = pd.DataFrame([customer_data])
    X = input_df[FEATURE_COLS].copy()

    churn_probability = float(pipeline.predict_proba(X)[0, 1])
    risk = risk_segment(churn_probability)

    result = {
        "customer_id": customer_data.get("customer_id"),
        "churn_probability": churn_probability,
        "risk_segment": risk,
        "estimated_revenue_at_risk": float(
            customer_data["monthly_charges"] * churn_probability
        ),
        "model_name": "XGBoost",
    }

    return result

def predict_single_by_id(customer_id: str) -> dict:
    df = load_customer_by_id(customer_id)

    if df.empty:
        raise ValueError(f"Customer ID {customer_id} not found.")

    row = df.iloc[0].to_dict()
    return predict_single(row)


def save_predictions_to_sql(predictions: pd.DataFrame, table_name: str = "predictions") -> None:
    engine = get_engine()

    # table_name = f"{table_name_prefix}_{TIMESTAMP}"

    predictions.to_sql(
        table_name,
        engine,
        if_exists="replace",        # set append in production
        index=False,
        chunksize=1000,
        method="multi",
    )

    log_file = PREDICTIONS_DIR / "prediction_table_log.txt"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{TIMESTAMP} -> {table_name}\n")

    print(f"Predictions saved to SQL table: {table_name}")
    print(f"SQL table log updated at: {log_file}")


def save_predictions_to_csv(predictions: pd.DataFrame) -> None:

    file_path = PREDICTIONS_DIR / f"predictions_{TIMESTAMP}.csv"

    predictions.to_csv(file_path, index=False)

    print(f"Predictions saved to: {file_path}")


def run_prediction_pipeline() -> pd.DataFrame:
    df = load_model_features()
    predictions = generate_predictions(df)
    save_predictions_to_sql(predictions)
    save_predictions_to_csv(predictions)
    return predictions


if __name__ == "__main__":
    predictions = run_prediction_pipeline()
    print(predictions.head())
