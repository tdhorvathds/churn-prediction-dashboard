from pathlib import Path
import pandas as pd

RAW_STREAM_PATH = Path("data/raw/synthetic_stream.csv")



def save_raw_record(record: dict):
    df = pd.DataFrame([record])

    RAW_STREAM_PATH.parent.mkdir(parents=True, exist_ok=True)

    if RAW_STREAM_PATH.exists():
        df.to_csv(RAW_STREAM_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(RAW_STREAM_PATH, mode="w", header=True, index=False)
