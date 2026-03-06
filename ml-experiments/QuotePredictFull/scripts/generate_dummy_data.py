from __future__ import annotations

import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import fitz


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.storage import init_db, insert_quote, delete_quotes_by_source  # noqa: E402
from src.train_model import train_and_save_model  # noqa: E402


PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "historical_quotes.csv"
MANIFEST_PATH = PROJECT_ROOT / "data" / "sample_manifest.csv"
DUMMY_PDF_DIR = PROJECT_ROOT / "data" / "raw" / "dummy_quotes"
DUMMY_SOURCE_TYPE = "dummy_generated"

RISK_SENTENCES = [
    "Includes unlimited liability obligations.",
    "Contains a penalty clause for late completion.",
    "Uses liquidated damages wording.",
    "Allows termination for convenience by buyer.",
    "Applies exclusive jurisdiction in buyer court.",
    "Includes non-standard warranty period.",
    "Includes late delivery penalty terms.",
]


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-x))


def _write_quote_pdf(pdf_path: Path, row: pd.Series) -> None:
    lines = [
        f"Quote ID: {row['QuoteID']}",
        f"Industry: {row['Industry']}",
        f"Total Price: SEK {row['TotalPrice']:,.2f}",
        f"Delivery Time: {int(row['DeliveryTime'])} days",
        "",
        "Commercial terms:",
    ]

    risk_count = int(row["RiskClauses"])
    if risk_count <= 0:
        lines.append("- Standard terms apply.")
    else:
        for idx in range(risk_count):
            lines.append(f"- {RISK_SENTENCES[idx % len(RISK_SENTENCES)]}")

    lines.extend(
        [
            "",
            "Decision history:",
            "Won quote." if int(row["Won_Quote"]) == 1 else "Lost quote.",
        ]
    )

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "\n".join(lines), fontsize=11)
    doc.save(pdf_path)
    doc.close()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate dummy quote data for QuotePredictFull.")
    parser.add_argument("--rows", type=int, default=100, help="Number of CSV rows to generate.")
    parser.add_argument("--pdf-count", type=int, default=30, help="How many dummy PDFs to generate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--load-into-db",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Load generated dummy data into SQLite automatically.",
    )
    parser.add_argument(
        "--train-after-load",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Train model automatically after dummy data has been loaded into DB.",
    )
    parser.add_argument(
        "--replace-existing-dummy",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Delete previous dummy-generated DB rows before inserting new ones.",
    )
    return parser


def _load_rows_into_database(df: pd.DataFrame, pdf_count: int, replace_existing_dummy: bool) -> tuple[int, int]:
    init_db()
    deleted = delete_quotes_by_source(DUMMY_SOURCE_TYPE) if replace_existing_dummy else 0

    inserted = 0
    for idx, row in df.iterrows():
        quote_id = str(row["QuoteID"]).lower()
        has_pdf = idx < pdf_count

        if has_pdf:
            filename = f"{quote_id}.pdf"
            pdf_path = str(DUMMY_PDF_DIR / filename)
        else:
            filename = f"{quote_id}.csv"
            pdf_path = ""

        features = {
            "TotalPrice": float(row["TotalPrice"]),
            "DeliveryTime": int(row["DeliveryTime"]),
            "Industry": str(row["Industry"]),
            "RiskClauses": int(row["RiskClauses"]),
        }

        insert_quote(
            filename=filename,
            pdf_path=pdf_path,
            source_type=DUMMY_SOURCE_TYPE,
            features=features,
            outcome=int(row["Won_Quote"]),
            predicted_label=None,
            predicted_probability=None,
            verified=True,
        )
        inserted += 1

    return inserted, deleted


def main() -> None:
    args = _build_parser().parse_args()
    rng = np.random.default_rng(args.seed)

    industries = [
        "Manufacturing",
        "Energy",
        "Construction",
        "Healthcare",
        "Retail",
        "Technology",
        "Public Sector",
    ]

    industry_bonus = {
        "Manufacturing": 0.2,
        "Energy": 0.0,
        "Construction": -0.3,
        "Healthcare": 0.4,
        "Retail": -0.2,
        "Technology": 0.5,
        "Public Sector": -0.1,
    }

    rows = []

    for i in range(args.rows):
        industry = rng.choice(industries)
        total_price = round(rng.uniform(200_000, 5_000_000), 2)
        delivery_time = int(rng.integers(7, 181))
        risk_clauses = int(rng.poisson(lam=2))

        score = (
            2.2
            - 0.00000035 * total_price
            - 0.008 * delivery_time
            - 0.5 * risk_clauses
            + industry_bonus[industry]
            + rng.normal(0, 0.4)
        )

        won_quote = int(rng.random() < sigmoid(score))

        rows.append(
            {
                "QuoteID": f"Q-{i+1:03d}",
                "TotalPrice": total_price,
                "DeliveryTime": delivery_time,
                "Industry": industry,
                "RiskClauses": risk_clauses,
                "Won_Quote": won_quote,
            }
        )

    df = pd.DataFrame(rows)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    DUMMY_PDF_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    pdf_count = min(max(0, args.pdf_count), len(df))
    for _, row in df.head(pdf_count).iterrows():
        filename = f"{str(row['QuoteID']).lower()}.pdf"
        pdf_path = DUMMY_PDF_DIR / filename
        _write_quote_pdf(pdf_path, row)
        manifest_rows.append({"filename": filename, "Won_Quote": int(row["Won_Quote"])})

    manifest_df = pd.DataFrame(manifest_rows)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    manifest_df.to_csv(MANIFEST_PATH, index=False)

    print(f"Saved {len(df)} rows to {PROCESSED_PATH}")
    print(f"Saved {len(manifest_df)} dummy PDFs to {DUMMY_PDF_DIR}")
    print(f"Saved manifest to {MANIFEST_PATH}")

    if args.load_into_db:
        inserted, deleted = _load_rows_into_database(df, pdf_count, args.replace_existing_dummy)
        print(f"Loaded {inserted} dummy rows into DB (deleted old dummy rows: {deleted}).")

        if args.train_after_load:
            metrics = train_and_save_model()
            print(
                "Model trained from DB:",
                {
                    "accuracy": round(metrics["accuracy"], 3),
                    "roc_auc": None if metrics["roc_auc"] is None else round(metrics["roc_auc"], 3),
                    "num_rows": metrics["num_rows"],
                },
            )


if __name__ == "__main__":
    main()
