from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = DATA_DIR / "models"
PROCESSED_DIR = DATA_DIR / "processed"
RAW_DIR = DATA_DIR / "raw"
RAW_QUOTES_DIR = RAW_DIR / "quotes"

DB_PATH = DATA_DIR / "app.db"
MODEL_PATH = MODELS_DIR / "quote_model.joblib"

# Backward-compatible fallback from previous hardcoded relative paths.
LEGACY_DATA_DIR = PROJECT_ROOT / "coding-playground" / "ml-experiments" / "QuotePredictFull" / "data"
LEGACY_DB_PATH = LEGACY_DATA_DIR / "app.db"
LEGACY_MODEL_PATH = LEGACY_DATA_DIR / "models" / "quote_model.joblib"
