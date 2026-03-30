import pandas as pd

from config import MODEL_DIR, PREDICTIONS_DIR
from data_loader import load_model_features, get_engine
from preprocessing import FEATURE_COLS
from utils import load_pipeline

TIMESTAMP = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")

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
