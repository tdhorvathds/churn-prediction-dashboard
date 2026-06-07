import joblib
import pandas as pd

from src.preprocessing import FEATURE_COLS
from src.config import MODEL_DIR, SYNTHETIC_PREDICTIONS_PATH, RAW_STREAM_PATH

def risk_segment(probability: float) -> str:
    if probability > 0.7:
        return "High"
    elif probability > 0.4:
        return "Medium"
    else:
        return "Low"


def load_latest_pipeline():
    model_files = sorted(MODEL_DIR.glob("churn_pipeline_*.pkl"))
    if not model_files:
        raise FileNotFoundError("No trained pipeline found in outputs/models")
    latest_model = model_files[-1]
    return joblib.load(latest_model), latest_model.name


def load_raw_stream() -> pd.DataFrame:
    if not RAW_STREAM_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(RAW_STREAM_PATH)


def load_existing_predictions() -> pd.DataFrame:
    if not SYNTHETIC_PREDICTIONS_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(SYNTHETIC_PREDICTIONS_PATH)


def get_unscored_batch(batch_size: int = 100) -> pd.DataFrame:
    raw_df = load_raw_stream()
    if raw_df.empty:
        return pd.DataFrame()

    pred_df = load_existing_predictions()

    if pred_df.empty or "customer_id" not in pred_df.columns:
        unscored_df = raw_df.copy()
    else:
        scored_ids = set(pred_df["customer_id"].astype(str))
        unscored_df = raw_df[~raw_df["customer_id"].astype(str).isin(scored_ids)].copy()

    if unscored_df.empty:
        return pd.DataFrame()

    return unscored_df.head(batch_size)


def generate_batch_predictions(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    pipeline, model_name = load_latest_pipeline()

    X = df[FEATURE_COLS].copy()
    churn_probabilities = pipeline.predict_proba(X)[:, 1]

    predictions = df.copy()
    predictions["churn_probability"] = churn_probabilities
    predictions["predicted_on"] = pd.Timestamp.now()
    predictions["risk_segment"] = predictions["churn_probability"].apply(risk_segment)
    predictions["estimated_revenue_at_risk"] = (
        predictions["monthly_charges"] * predictions["churn_probability"]
    )
    predictions["model_name"] = model_name

    return predictions[
        [
            "customer_id",
            "timestamp",
            "churn_probability",
            "risk_segment",
            "estimated_revenue_at_risk",
            "predicted_on",
            "model_name",
        ]
    ].copy()


def save_prediction_batch(predictions: pd.DataFrame) -> None:
    if predictions.empty:
        return

    SYNTHETIC_PREDICTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)

    if SYNTHETIC_PREDICTIONS_PATH.exists():
        predictions.to_csv(SYNTHETIC_PREDICTIONS_PATH, mode="a", header=False, index=False)
    else:
        predictions.to_csv(SYNTHETIC_PREDICTIONS_PATH, mode="w", header=True, index=False)


def run_batch_if_ready(batch_size: int = 100) -> int:
    batch_df = get_unscored_batch(batch_size=batch_size)

    if len(batch_df) < batch_size:
        return 0

    predictions = generate_batch_predictions(batch_df)
    save_prediction_batch(predictions)

    return len(predictions)