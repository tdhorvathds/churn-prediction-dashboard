import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

from src.data_loader import load_model_features

NUM_COLS = [
    "senior_citizen",
    "partner",
    "dependents",
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "phone_service",
    "multiple_lines",
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_tv",
    "streaming_movies",
]

CAT_COLS = [
    "gender",
    "city",
    "contract_type",
    "payment_method",
    "internet_service"
]

FEATURE_COLS = NUM_COLS + CAT_COLS

TARGET_COL = "churn_value"

def load_training_data():
    df = load_model_features()

    X = df[NUM_COLS + CAT_COLS]
    y = df[TARGET_COL]

    return X, y

def create_preprocessor():

    numeric_transformer = Pipeline([
        ("Scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ("Onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers = [
            ("num", numeric_transformer, NUM_COLS),
            ("cat", categorical_transformer, CAT_COLS)
        ]
    )

    return preprocessor

def get_feature_names(preprocessor):
    return preprocessor.get_feature_names_out()