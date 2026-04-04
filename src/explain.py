import shap
import pandas as pd
from scipy import sparse
import matplotlib.pyplot as plt

from src.config import EXPLAIN_DIR
from src.data_loader import load_model_features
from src.preprocessing import FEATURE_COLS
from src.utils import load_pipeline
from src.predict import risk_segment
from src.recommend import recommend_actions

def load_explain_data() -> pd.DataFrame:
    df = load_model_features()
    return df.copy()


def get_preprocessor_and_model():
    pipeline = load_pipeline()
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    return preprocessor, model


def prepare_transformed_features(df: pd.DataFrame):
    preprocessor, model = get_preprocessor_and_model()

    X = df[FEATURE_COLS].copy()
    X_transformed = preprocessor.transform(X)
    feature_names = preprocessor.get_feature_names_out()

    if sparse.issparse(X_transformed):
        X_transformed_df = pd.DataFrame.sparse.from_spmatrix(
            X_transformed,
            columns=feature_names,
            index=df.index
        )
    else:
        X_transformed_df = pd.DataFrame(
            X_transformed,
            columns=feature_names,
            index=df.index
        )

    return X, X_transformed_df, preprocessor, model


def clean_feature_name(feature_name: str) -> str:
    if feature_name.startswith("num__"):
        return feature_name.replace("num__", "")

    if feature_name.startswith("cat__"):
        cleaned = feature_name.replace("cat__", "")

        categorical_prefixes = [
            "gender",
            "city",
            "contract_type",
            "payment_method",
            "internet_service"
        ]

        for prefix in categorical_prefixes:
            prefix_with_sep = f"{prefix}_"

            if cleaned.startswith(prefix_with_sep):
                value = cleaned.replace(prefix_with_sep, "")
                return f"{prefix} = {value}"

        return cleaned

    return feature_name


def aggregate_shap_features(explanation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Group one-hot encoded SHAP features into logical feature families
    to make explanations easier to interpret.
    """

    grouped_rows = []

    for _, row in explanation_df.iterrows():
        feature = row["feature"]
        shap_value = row["shap_value"]

        if feature.startswith("city = "):
            grouped_feature = "city"

        elif feature.startswith("contract_type = "):
            grouped_feature = "contract_type"

        elif feature.startswith("payment_method = "):
            grouped_feature = "payment_method"

        elif feature.startswith("internet_service = "):
            grouped_feature = "internet_service"

        elif feature.startswith("gender = "):
            grouped_feature = "gender"

        else:
            grouped_feature = feature

        grouped_rows.append(
            {
                "feature": grouped_feature,
                "shap_value": shap_value
            }
        )

    grouped_df = (
        pd.DataFrame(grouped_rows)
        .groupby("feature", as_index=False)["shap_value"]
        .sum()
    )

    grouped_df["abs_shap_value"] = grouped_df["shap_value"].abs()

    return grouped_df.sort_values("abs_shap_value", ascending=False)


def build_explainer(background_df: pd.DataFrame = None):
    df = load_explain_data()
    X, X_transformed_df, _, model = prepare_transformed_features(df)

    if background_df is None:
        background_df = X_transformed_df.sample(
            min(200, len(X_transformed_df)),
            random_state=42
        )

    explainer = shap.TreeExplainer(model,
                                   data=background_df)

    return explainer, X_transformed_df, X


def get_shap_values():
    explainer, X_transformed_df, X_raw = build_explainer()
    shap_values = explainer.shap_values(X_transformed_df)

    return shap_values, X_transformed_df, X_raw


def save_global_importance_bar():
    EXPLAIN_DIR.mkdir(parents=True, exist_ok=True)

    shap_values, X_transformed_df, _ = get_shap_values()

    plt.figure()
    shap.summary_plot(
        shap_values,
        X_transformed_df,
        plot_type="bar",
        show=False
    )

    output_path = EXPLAIN_DIR / "global_importance_bar.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output_path}")


def save_global_beeswarm():
    EXPLAIN_DIR.mkdir(parents=True, exist_ok=True)

    shap_values, X_transformed_df, _ = get_shap_values()

    plt.figure()
    shap.summary_plot(
        shap_values,
        X_transformed_df,
        show=False
    )

    output_path = EXPLAIN_DIR / "global_beeswarm.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output_path}")


def explain_single_customer(customer_id):
    df = load_explain_data()
    shap_values, X_transformed_df, X_raw = get_shap_values()

    if "customer_id" not in df.columns:
        raise ValueError("customer_id column not found in source data.")

    row = df[df["customer_id"] == customer_id]

    if row.empty:
        raise ValueError(f"Customer ID {customer_id} not found.")

    row_index = row.index[0]

    row_raw = X_raw.loc[[row_index]]
    row_transformed = X_transformed_df.loc[[row_index]]

    prediction_pipeline = load_pipeline()
    churn_probability = prediction_pipeline.predict_proba(row_raw)[0, 1]

    row_shap = shap_values[row_index]

    explanation_df = pd.DataFrame({
        "feature": X_transformed_df.columns,
        "shap_value": row_shap,
        "abs_shap_value": abs(row_shap)
    }).sort_values("abs_shap_value", ascending=False)

    explanation_df["feature"] = explanation_df["feature"].apply(clean_feature_name)
    explanation_df["customer_id"] = customer_id
    explanation_df["churn_probability"] = churn_probability

    return explanation_df, row_transformed, churn_probability


def explain_single_customer_summary(customer_id: str, top_n: int = 5) -> dict:
    df = load_explain_data()
    customer_row = df[df["customer_id"] == customer_id]

    if customer_row.empty:
        raise ValueError(f"Customer ID {customer_id} not found.")

    customer_data = customer_row.iloc[0].to_dict()

    explanation_df, _, churn_probability = explain_single_customer(customer_id)
    grouped_explanation_df = aggregate_shap_features(explanation_df)

    positive_drivers = (
        grouped_explanation_df[grouped_explanation_df["shap_value"] > 0]
        .sort_values("shap_value", ascending=False)
        .head(top_n)[["feature", "shap_value"]]
        .to_dict(orient="records")
    )

    negative_drivers = (
        grouped_explanation_df[grouped_explanation_df["shap_value"] < 0]
        .sort_values("shap_value", ascending=True)
        .head(top_n)[["feature", "shap_value"]]
        .to_dict(orient="records")
    )

    recommendations = recommend_actions(
        churn_probability=float(churn_probability),
        risk_segment=risk_segment(float(churn_probability)),
        top_risk_drivers=positive_drivers,
        customer_data=customer_data
    )

    return {
        "customer_id": customer_id,
        "churn_probability": float(churn_probability),
        "top_risk_drivers": positive_drivers,
        "top_protective_drivers": negative_drivers,
        "recommended_actions": recommendations
    }


def save_single_customer_explanation(customer_id):
    EXPLAIN_DIR.mkdir(parents=True, exist_ok=True)

    explanation_df, row_transformed, churn_probability = explain_single_customer(customer_id)

    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    csv_path = EXPLAIN_DIR / f"customer_{customer_id}_explanation_{timestamp}.csv"
    png_path = EXPLAIN_DIR / f"customer_{customer_id}_waterfall_{timestamp}.png"

    explanation_df.to_csv(csv_path, index=False)

    top_n = explanation_df.head(10)
    print(top_n)

    explainer, X_transformed_df, _ = build_explainer()
    shap_values = explainer.shap_values(X_transformed_df)

    original_df = load_explain_data()
    row = original_df[original_df["customer_id"] == customer_id]
    row_index = row.index[0]

    shap_explanation = shap.Explanation(
        values=shap_values[row_index],
        base_values=explainer.expected_value,
        data=X_transformed_df.loc[row_index].values,
        feature_names=X_transformed_df.columns.tolist()
    )

    plt.figure()
    shap.plots.waterfall(shap_explanation, max_display=10, show=False)
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved CSV: {csv_path}")
    print(f"Saved waterfall plot: {png_path}")
    print(f"Churn probability: {churn_probability:.4f}")


def explain_customer_payload(customer_data: dict, top_n: int = 5) -> dict:
    preprocessor, model = get_preprocessor_and_model()

    input_df = pd.DataFrame([customer_data])
    X_raw = input_df[FEATURE_COLS].copy()

    X_transformed = preprocessor.transform(X_raw)
    feature_names = preprocessor.get_feature_names_out()

    if sparse.issparse(X_transformed):
        X_transformed_df = pd.DataFrame.sparse.from_spmatrix(
            X_transformed,
            columns=feature_names
        )
    else:
        X_transformed_df = pd.DataFrame(
            X_transformed,
            columns=feature_names
        )

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_transformed_df)

    if isinstance(shap_values, list):
        shap_row = shap_values[1][0]
    else:
        shap_row = shap_values[0]

    prediction_pipeline = load_pipeline()
    churn_probability = float(
        prediction_pipeline.predict_proba(X_raw)[0, 1]
    )

    explanation_df = pd.DataFrame({
        "feature": X_transformed_df.columns,
        "shap_value": shap_row,
    })

    explanation_df["abs_shap_value"] = explanation_df["shap_value"].abs()
    explanation_df["feature"] = explanation_df["feature"].apply(clean_feature_name)

    grouped_explanation_df = aggregate_shap_features(explanation_df)

    positive_drivers = (
        grouped_explanation_df[grouped_explanation_df["shap_value"] > 0]
        .sort_values("shap_value", ascending=False)
        .head(top_n)[["feature", "shap_value"]]
        .to_dict(orient="records")
    )

    negative_drivers = (
        grouped_explanation_df[grouped_explanation_df["shap_value"] < 0]
        .sort_values("shap_value", ascending=True)
        .head(top_n)[["feature", "shap_value"]]
        .to_dict(orient="records")
    )

    recommendations = recommend_actions(
        churn_probability=churn_probability,
        risk_segment=risk_segment(churn_probability),
        top_risk_drivers=positive_drivers,
        customer_data=customer_data
    )

    return {
        "customer_id": customer_data.get("customer_id"),
        "churn_probability": churn_probability,
        "top_risk_drivers": positive_drivers,
        "top_protective_drivers": negative_drivers,
        "recommended_actions": recommendations
    }


def run_explainability_pipeline(sample_customer_id=None):
    save_global_importance_bar()
    save_global_beeswarm()

    if sample_customer_id is not None:
        save_single_customer_explanation(sample_customer_id)


if __name__ == "__main__":
    df = load_explain_data()

    row_count = len(df)
    print(f"Loaded {row_count} rows for explainability.")

    sample_customer_id = df["customer_id"].sample(1, random_state=42).iloc[0]

    print(f"Using random sample customer_id: {sample_customer_id}")

    run_explainability_pipeline(sample_customer_id=sample_customer_id)