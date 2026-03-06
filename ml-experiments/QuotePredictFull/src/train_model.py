from __future__ import annotations

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

from src.paths import MODEL_PATH
from src.storage import get_training_dataframe

FEATURE_COLUMNS = ["TotalPrice", "DeliveryTime", "Industry", "RiskClauses"]


def _validate_training_data(df: pd.DataFrame) -> None:
    required = set(FEATURE_COLUMNS + ["Won_Quote"])
    missing = required - set(df.columns)
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise ValueError(f"Training data is missing required columns: {missing_str}")

    if len(df) < 10:
        raise ValueError("Not enough labeled quotes to train the model. Need at least 10.")

    class_counts = df["Won_Quote"].value_counts(dropna=True)
    if len(class_counts) < 2:
        raise ValueError("Model training needs both classes (Won_Quote=0 and Won_Quote=1).")

    if int(class_counts.min()) < 2:
        raise ValueError("Each class needs at least 2 samples to train/test split reliably.")


def train_and_save_model() -> dict:
    df = get_training_dataframe()
    _validate_training_data(df)

    X = df[FEATURE_COLUMNS]
    y = df["Won_Quote"]

    numeric_features = ["TotalPrice", "DeliveryTime", "RiskClauses"]
    categorical_features = ["Industry"]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                ]),
                numeric_features,
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]),
                categorical_features,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )

    test_size = 0.2 if len(df) >= 20 else max(0.25, 4 / len(df))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    roc_auc = float(roc_auc_score(y_test, y_prob)) if len(set(y_test)) > 1 else None

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "roc_auc": roc_auc,
        "report": classification_report(y_test, y_pred, zero_division=0),
        "num_rows": int(len(df)),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "feature_columns": FEATURE_COLUMNS,
        },
        MODEL_PATH,
    )

    return metrics


if __name__ == "__main__":
    metrics = train_and_save_model()
    print("Model trained and saved.")
    print(metrics)
