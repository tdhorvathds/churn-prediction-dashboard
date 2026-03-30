import pandas as pd
from sqlalchemy import create_engine
from src.config import DB_URL


def get_engine():
    return create_engine(DB_URL)


def load_model_features() -> pd.DataFrame:
    engine = get_engine()

    query = """
    SELECT *
    FROM model_features
    """

    df = pd.read_sql(query, engine)
    return df