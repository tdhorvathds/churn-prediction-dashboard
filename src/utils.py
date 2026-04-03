import joblib

from src.config import MODEL_DIR

MODEL_PATH = MODEL_DIR / "churn_pipeline_20260403_152940.pkl"

def load_pipeline():
    return joblib.load(MODEL_PATH)

