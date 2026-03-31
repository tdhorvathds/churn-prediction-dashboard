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

def load_customer_by_id(customer_id: str) -> pd.DataFrame:
    engine = get_engine()

    query = """
    SELECT *
    FROM model_features
    WHERE customer_id = %(customer_id)s
    """

    df = pd.read_sql(query, engine, params={"customer_id": customer_id})
    return df