from pathlib import Path
import pandas as pd

from src.config import RAW_STREAM_PATH


def save_raw_record(record: dict):
    df = pd.DataFrame([record])

    RAW_STREAM_PATH.parent.mkdir(parents=True, exist_ok=True)

    if RAW_STREAM_PATH.exists():
        df.to_csv(RAW_STREAM_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(RAW_STREAM_PATH, mode="w", header=True, index=False)
