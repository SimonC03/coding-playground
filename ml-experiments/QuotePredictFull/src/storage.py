from __future__ import annotations

import sqlite3
import shutil
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import pandas as pd

from src.paths import DB_PATH, RAW_QUOTES_DIR, LEGACY_DB_PATH

PDF_DIR = RAW_QUOTES_DIR
STRUCTURED_REQUIRED_COLUMNS = {"TotalPrice", "DeliveryTime", "Industry", "RiskClauses", "Won_Quote"}


def _migrate_legacy_db_if_needed() -> None:
    if DB_PATH.exists() or not LEGACY_DB_PATH.exists():
        return
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(LEGACY_DB_PATH, DB_PATH)


def get_connection() -> sqlite3.Connection:
    _migrate_legacy_db_if_needed()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                pdf_path TEXT NOT NULL,
                source_type TEXT NOT NULL,
                total_price REAL,
                delivery_time INTEGER,
                industry TEXT,
                risk_clauses INTEGER,
                outcome INTEGER,
                predicted_label INTEGER,
                predicted_probability REAL,
                verified INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def save_pdf_bytes(file_name: str, pdf_bytes: bytes) -> Path:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file_name).name
    file_path = PDF_DIR / safe_name
    file_path.write_bytes(pdf_bytes)
    return file_path


def insert_quote(
    filename: str,
    pdf_path: str,
    source_type: str,
    features: Dict[str, Any],
    outcome: Optional[int] = None,
    predicted_label: Optional[int] = None,
    predicted_probability: Optional[float] = None,
    verified: bool = False,
) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO quotes (
                filename, pdf_path, source_type,
                total_price, delivery_time, industry, risk_clauses,
                outcome, predicted_label, predicted_probability, verified
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                pdf_path,
                source_type,
                features.get("TotalPrice"),
                features.get("DeliveryTime"),
                features.get("Industry"),
                features.get("RiskClauses"),
                outcome,
                predicted_label,
                predicted_probability,
                int(verified),
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def list_quotes() -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query(
            """
            SELECT
                id, filename, source_type,
                total_price, delivery_time, industry, risk_clauses,
                outcome, predicted_label, predicted_probability,
                verified, created_at
            FROM quotes
            ORDER BY created_at DESC, id DESC
            """,
            conn,
        )


def get_quote(quote_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,)).fetchone()
    return dict(row) if row else None


def update_outcome(quote_id: int, outcome: int) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE quotes
            SET outcome = ?, verified = 1
            WHERE id = ?
            """,
            (outcome, quote_id),
        )
        conn.commit()


def get_training_dataframe() -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query(
            """
            SELECT
                total_price AS TotalPrice,
                delivery_time AS DeliveryTime,
                industry AS Industry,
                risk_clauses AS RiskClauses,
                outcome AS Won_Quote
            FROM quotes
            WHERE outcome IS NOT NULL
            """,
            conn,
        )


def get_stats() -> Dict[str, int]:
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
        labeled = conn.execute("SELECT COUNT(*) FROM quotes WHERE outcome IS NOT NULL").fetchone()[0]
        predictions = conn.execute("SELECT COUNT(*) FROM quotes WHERE source_type = 'prediction'").fetchone()[0]
        historical = conn.execute("SELECT COUNT(*) FROM quotes WHERE source_type = 'historical'").fetchone()[0]
        historical_csv = conn.execute("SELECT COUNT(*) FROM quotes WHERE source_type = 'historical_csv'").fetchone()[0]
        dummy_generated = conn.execute("SELECT COUNT(*) FROM quotes WHERE source_type = 'dummy_generated'").fetchone()[0]
    return {
        "total_quotes": int(total),
        "labeled_quotes": int(labeled),
        "prediction_quotes": int(predictions),
        "historical_quotes": int(historical),
        "historical_csv_quotes": int(historical_csv),
        "dummy_generated_quotes": int(dummy_generated),
    }


def delete_quotes_by_source(source_type: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM quotes WHERE source_type = ?", (source_type,))
        conn.commit()
        return int(cursor.rowcount if cursor.rowcount is not None else 0)


def _coerce_optional_float(value: Any) -> Optional[float]:
    if pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coerce_optional_int(value: Any) -> Optional[int]:
    if pd.isna(value):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _coerce_outcome(value: Any) -> Optional[int]:
    coerced = _coerce_optional_int(value)
    if coerced not in (0, 1):
        return None
    return coerced


def _derive_filename(row: pd.Series, index: int) -> str:
    for key in ("filename", "Filename", "QuoteID", "QuoteId", "quote_id"):
        if key in row and not pd.isna(row[key]):
            candidate = str(row[key]).strip()
            if candidate:
                return Path(candidate).name
    return f"csv_quote_{index + 1:05d}.csv"


def insert_structured_csv(df: pd.DataFrame, source_type: str = "historical_csv") -> Tuple[int, int]:
    missing_cols = STRUCTURED_REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        missing = ", ".join(sorted(missing_cols))
        raise ValueError(f"CSV is missing required columns: {missing}")

    inserted = 0
    skipped = 0

    for idx, row in df.iterrows():
        outcome = _coerce_outcome(row.get("Won_Quote"))
        if outcome is None:
            skipped += 1
            continue

        features = {
            "TotalPrice": _coerce_optional_float(row.get("TotalPrice")),
            "DeliveryTime": _coerce_optional_int(row.get("DeliveryTime")),
            "Industry": str(row.get("Industry")).strip() if not pd.isna(row.get("Industry")) else "Unknown",
            "RiskClauses": _coerce_optional_int(row.get("RiskClauses")),
        }

        insert_quote(
            filename=_derive_filename(row, idx),
            pdf_path="",
            source_type=source_type,
            features=features,
            outcome=outcome,
            predicted_label=None,
            predicted_probability=None,
            verified=True,
        )
        inserted += 1

    return inserted, skipped
