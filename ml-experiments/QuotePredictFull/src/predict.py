from __future__ import annotations

import shutil
import joblib
import pandas as pd

from src.paths import MODEL_PATH, LEGACY_MODEL_PATH


def load_model_bundle() -> dict:
    if not MODEL_PATH.exists() and LEGACY_MODEL_PATH.exists():
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(LEGACY_MODEL_PATH, MODEL_PATH)
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Train the model first.")
    return joblib.load(MODEL_PATH)


def predict_quote(features: dict) -> dict:
    bundle = load_model_bundle()
    feature_columns = bundle["feature_columns"]
    model = bundle["model"]

    input_df = pd.DataFrame([features])[feature_columns]
    predicted_label = int(model.predict(input_df)[0])
    predicted_probability = float(model.predict_proba(input_df)[0][1])

    return {
        "predicted_label": predicted_label,
        "predicted_probability": predicted_probability,
    }
