import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, roc_auc_score, classification_report, confusion_matrix
from xgboost import XGBClassifier

from config import MODEL_DIR
from preprocessing import load_training_data, create_preprocessor

MODEL_PATH = MODEL_DIR / "churn_pipeline.pkl"

def build_model():
    model = Pipeline(
        steps = [
            ("preprocessor", create_preprocessor()),
            (
                "model",
                XGBClassifier(
                    n_estimators=200,
                    max_depth=5,
                    learning_rate=0.05,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    random_state=42,
                    eval_metric="logloss"
                )
            )
        ]
    )

    return model

def train_model():
    X, y = load_training_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = build_model()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("\nROC-AUC Score:")
    print(roc_auc_score(y_test, y_proba))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")

    return model, X_train, X_test, y_train, y_test

if __name__ == "__main__":
    train_model()