from pathlib import Path
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DB_URL = os.getenv("DB_URL")

DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"

MODEL_DIR = OUTPUTS_DIR / "models"
EXPLAIN_DIR = OUTPUTS_DIR / "explainability"
PREDICTIONS_DIR = OUTPUTS_DIR / "predictions"

TIMESTAMP = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")