import joblib
import pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import precision_score, recall_score, roc_auc_score, classification_report, confusion_matrix
from xgboost import XGBClassifier

from src.config import MODEL_DIR, TIMESTAMP
from src.preprocessing import load_training_data, create_preprocessor


MODEL_PATH = MODEL_DIR / f"churn_pipeline_{TIMESTAMP}.pkl"
PARAM_PATH = MODEL_DIR / f"best_parameters_{TIMESTAMP}.csv"

def build_model():
    pipeline = Pipeline(
        steps = [
            ("preprocessor", create_preprocessor()),
            (
                "model",
                XGBClassifier(
                    random_state=42,
                    eval_metric="logloss"
                )
            )
        ]
    )

    param_grid = {
        "model__n_estimators": [100, 200, 300, 500],
        "model__max_depth": [3, 4, 5, 6, 8],
        "model__learning_rate": [0.01, 0.03, 0.05, 0.1],
        "model__subsample": [0.6, 0.8, 1.0],
        "model__colsample_bytree": [0.6, 0.8, 1.0],
        "model__min_child_weight": [1, 3, 5],
        "model__gamma": [0, 0.1, 0.3, 0.5],
    }

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_grid,
        n_iter=20,
        scoring="roc_auc",
        cv=5,
        verbose=2,
        n_jobs=-1,
        random_state=42
    )

    return search


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

    print("Best parameters:")
    print(model.best_params_)

    best_params = pd.DataFrame(list(model.best_params_.items()), columns=["parameter", "value"])

    best_params.to_csv(PARAM_PATH, index=False, sep = ',', encoding='utf-8')

    print(f"Best parameters saved to: {PARAM_PATH}")

    print("Best cross-validated ROC-AUC:")
    print(model.best_score_)

    best_model = model.best_estimator_

    y_pred = best_model.predict(X_test)
    y_proba = best_model.predict_proba(X_test)[:, 1]

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("\nTest ROC-AUC Score:")
    print(roc_auc_score(y_test, y_proba))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")

    return best_model, model, X_train, X_test, y_train, y_test

if __name__ == "__main__":
    train_model()