from pathlib import Path
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DB_URL = os.getenv("DB_URL")

DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"

LOG_DIR = OUTPUTS_DIR / "logs"
MODEL_DIR = OUTPUTS_DIR / "models"
EXPLAIN_DIR = OUTPUTS_DIR / "explainability"
PREDICTIONS_DIR = OUTPUTS_DIR / "predictions"
SYNTHETIC_PREDICTIONS_PATH = PREDICTIONS_DIR / "stream_predictions.csv"
RAW_STREAM_PATH = DATA_DIR / "raw/synthetic_stream.csv"

TIMESTAMP = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")