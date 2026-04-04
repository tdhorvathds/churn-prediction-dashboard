import joblib

from src.config import MODEL_DIR

MODEL_PATH = MODEL_DIR / "churn_pipeline_20260404_114814.pkl"

def load_pipeline():
    return joblib.load(MODEL_PATH)

