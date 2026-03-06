from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

from src.extractor import extract_quote_features
from src.predict import predict_quote, load_model_bundle
from src.preview import render_first_page_as_png
from src.storage import (
    init_db,
    save_pdf_bytes,
    insert_quote,
    insert_structured_csv,
    list_quotes,
    get_quote,
    update_outcome,
    get_stats,
)
from src.train_model import train_and_save_model


def show_training_metrics(metrics: dict) -> None:
    st.write(
        {
            "accuracy": round(metrics["accuracy"], 3),
            "roc_auc": None if metrics["roc_auc"] is None else round(metrics["roc_auc"], 3),
            "num_rows": metrics["num_rows"],
        }
    )
    with st.expander("Classification report"):
        st.text(metrics["report"])


st.set_page_config(page_title="QuotePredict", layout="wide")
init_db()

st.title("QuotePredict")
st.caption("Upload B2B quote PDFs, extract structured keys, browse historical quotes, and predict win/loss.")

mode = st.sidebar.radio(
    "Mode",
    ["Import historical", "Browse quotes", "Predict", "Model admin"],
)

stats = get_stats()
with st.sidebar:
    st.markdown("### Database")
    st.write(f"Total quotes: {stats['total_quotes']}")
    st.write(f"Labeled quotes: {stats['labeled_quotes']}")
    st.write(f"Historical quotes: {stats['historical_quotes']}")
    st.write(f"Historical CSV quotes: {stats['historical_csv_quotes']}")
    st.write(f"Dummy generated quotes: {stats['dummy_generated_quotes']}")
    st.write(f"Prediction quotes: {stats['prediction_quotes']}")


if mode == "Import historical":
    st.header("Import historical quotes")
    st.write("Import either PDF+manifest or a structured CSV with key points and outcomes.")

    tab_pdf, tab_csv = st.tabs(["PDF + manifest", "Structured CSV"])

    with tab_pdf:
        st.subheader("Import historical PDFs")
        manifest_file = st.file_uploader("Upload manifest CSV", type=["csv"], key="manifest_csv_upload")
        pdf_files = st.file_uploader(
            "Upload historical PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            key="historical_pdf_upload",
        )
        retrain_after_pdf_import = st.checkbox("Retrain model after PDF import", value=True, key="retrain_pdf")

        if manifest_file is not None:
            try:
                manifest_df = pd.read_csv(manifest_file)
                manifest_df["Won_Quote"] = pd.to_numeric(manifest_df.get("Won_Quote"), errors="coerce")
                st.subheader("Manifest preview")
                st.dataframe(manifest_df, use_container_width=True)
            except Exception as exc:
                manifest_df = None
                st.error(f"Could not read manifest CSV: {exc}")
        else:
            manifest_df = None

        if manifest_df is not None and pdf_files:
            required_cols = {"filename", "Won_Quote"}
            if not required_cols.issubset(manifest_df.columns):
                st.error("CSV must contain columns: filename, Won_Quote")
            elif st.button("Process and save historical PDFs", key="process_historical_pdfs"):
                outcome_map = dict(zip(manifest_df["filename"], manifest_df["Won_Quote"]))
                saved = 0
                skipped = []

                progress = st.progress(0)
                status = st.empty()

                for idx, pdf in enumerate(pdf_files, start=1):
                    status.write(f"Processing {pdf.name}...")
                    pdf_bytes = pdf.read()
                    features = extract_quote_features(pdf_bytes)
                    file_path = save_pdf_bytes(pdf.name, pdf_bytes)
                    outcome = outcome_map.get(pdf.name)

                    if pd.isna(outcome) or outcome not in (0, 1):
                        skipped.append(pdf.name)
                    else:
                        insert_quote(
                            filename=pdf.name,
                            pdf_path=str(file_path),
                            source_type="historical",
                            features=features,
                            outcome=int(outcome),
                            predicted_label=None,
                            predicted_probability=None,
                            verified=True,
                        )
                        saved += 1

                    progress.progress(idx / len(pdf_files))

                status.empty()
                st.success(f"Saved {saved} historical quotes from PDFs.")
                if skipped:
                    st.warning("Skipped quotes with missing/invalid labels: " + ", ".join(skipped))

                if retrain_after_pdf_import and saved > 0:
                    try:
                        metrics = train_and_save_model()
                        st.success("Model retrained after PDF import.")
                        show_training_metrics(metrics)
                    except Exception as exc:
                        st.warning(f"Imported data saved, but retraining failed: {exc}")

    with tab_csv:
        st.subheader("Import structured historical CSV")
        st.write("Required columns: TotalPrice, DeliveryTime, Industry, RiskClauses, Won_Quote")
        structured_csv = st.file_uploader(
            "Upload structured historical CSV",
            type=["csv"],
            key="structured_historical_csv_upload",
        )
        retrain_after_csv_import = st.checkbox("Retrain model after CSV import", value=True, key="retrain_csv")

        if structured_csv is not None:
            try:
                structured_df = pd.read_csv(structured_csv)
                st.subheader("Structured CSV preview")
                st.dataframe(structured_df, use_container_width=True)
            except Exception as exc:
                structured_df = None
                st.error(f"Could not read structured CSV: {exc}")
        else:
            structured_df = None

        if structured_df is not None:
            required_cols = {"TotalPrice", "DeliveryTime", "Industry", "RiskClauses", "Won_Quote"}
            missing_cols = required_cols - set(structured_df.columns)
            if missing_cols:
                st.error("CSV is missing required columns: " + ", ".join(sorted(missing_cols)))
            elif st.button("Import structured CSV rows", key="import_structured_rows"):
                try:
                    inserted, skipped = insert_structured_csv(structured_df, source_type="historical_csv")
                    st.success(f"Imported {inserted} rows from structured CSV.")
                    if skipped:
                        st.warning(f"Skipped {skipped} rows with invalid outcome.")

                    if retrain_after_csv_import and inserted > 0:
                        try:
                            metrics = train_and_save_model()
                            st.success("Model retrained after CSV import.")
                            show_training_metrics(metrics)
                        except Exception as exc:
                            st.warning(f"CSV imported, but retraining failed: {exc}")
                except Exception as exc:
                    st.error(str(exc))

elif mode == "Browse quotes":
    st.header("Browse stored quotes")
    df = list_quotes()

    if df.empty:
        st.info("No quotes stored yet.")
    else:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            source_filter = st.selectbox("Source type", ["All"] + sorted(df["source_type"].dropna().unique().tolist()))
        with col_f2:
            industry_filter = st.selectbox("Industry", ["All"] + sorted(df["industry"].fillna("Unknown").unique().tolist()))
        with col_f3:
            outcome_filter = st.selectbox("Outcome", ["All", "Won", "Lost", "Unknown"])

        filtered_df = df.copy()
        if source_filter != "All":
            filtered_df = filtered_df[filtered_df["source_type"] == source_filter]
        if industry_filter != "All":
            filtered_df = filtered_df[filtered_df["industry"].fillna("Unknown") == industry_filter]
        if outcome_filter == "Won":
            filtered_df = filtered_df[filtered_df["outcome"] == 1]
        elif outcome_filter == "Lost":
            filtered_df = filtered_df[filtered_df["outcome"] == 0]
        elif outcome_filter == "Unknown":
            filtered_df = filtered_df[filtered_df["outcome"].isna()]

        st.subheader("Quotes")
        st.dataframe(filtered_df, use_container_width=True)

        if not filtered_df.empty:
            selected_id = st.selectbox("Select quote ID", filtered_df["id"].tolist())
            record = get_quote(int(selected_id))

            if record:
                col1, col2 = st.columns([1.1, 1])

                with col1:
                    st.subheader(record["filename"])
                    pdf_path = str(record.get("pdf_path") or "").strip()
                    if pdf_path and Path(pdf_path).exists():
                        st.image(render_first_page_as_png(pdf_path), caption="First page preview")
                    elif pdf_path:
                        st.warning("Stored PDF file not found on disk.")
                    else:
                        st.info("No PDF attached to this quote (likely imported from structured CSV).")

                with col2:
                    st.subheader("Extracted keys")
                    st.json(
                        {
                            "TotalPrice": record["total_price"],
                            "DeliveryTime": record["delivery_time"],
                            "Industry": record["industry"],
                            "RiskClauses": record["risk_clauses"],
                        }
                    )

                    st.subheader("Outcome / prediction")
                    st.write("Ground truth outcome:", record["outcome"])
                    st.write("Predicted label:", record["predicted_label"])
                    st.write("Predicted probability:", record["predicted_probability"])
                    st.write("Verified:", bool(record["verified"]))

                    new_outcome = st.selectbox(
                        "Update true outcome",
                        options=[None, 0, 1],
                        format_func=lambda x: "Unknown" if x is None else ("Lost" if x == 0 else "Won"),
                        key=f"outcome_{record['id']}",
                    )
                    retrain_after_outcome = st.checkbox(
                        "Retrain model after saving outcome",
                        value=False,
                        key=f"retrain_outcome_{record['id']}",
                    )

                    if st.button("Save outcome", key=f"save_{record['id']}"):
                        if new_outcome is not None:
                            update_outcome(record["id"], int(new_outcome))
                            st.success("Outcome updated.")
                            if retrain_after_outcome:
                                try:
                                    metrics = train_and_save_model()
                                    st.success("Model retrained after outcome update.")
                                    show_training_metrics(metrics)
                                except Exception as exc:
                                    st.warning(f"Outcome saved, but retraining failed: {exc}")
                            st.rerun()

elif mode == "Predict":
    st.header("Predict a new quote")

    try:
        load_model_bundle()
    except FileNotFoundError:
        st.warning("No trained model found yet. Import historical data and train first.")
    else:
        uploaded_pdf = st.file_uploader("Upload a new PDF quote", type=["pdf"])

        if uploaded_pdf is not None:
            pdf_bytes = uploaded_pdf.read()
            features = extract_quote_features(pdf_bytes)
            prediction = predict_quote(features)

            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("Extracted keys")
                st.json(features)

            with col2:
                st.subheader("Prediction")
                label = "WIN" if prediction["predicted_label"] == 1 else "LOSS"
                st.metric("Predicted outcome", label)
                st.metric("Win probability", f"{prediction['predicted_probability']:.1%}")

            if st.button("Save quote to database"):
                file_path = save_pdf_bytes(uploaded_pdf.name, pdf_bytes)
                insert_quote(
                    filename=uploaded_pdf.name,
                    pdf_path=str(file_path),
                    source_type="prediction",
                    features=features,
                    outcome=None,
                    predicted_label=prediction["predicted_label"],
                    predicted_probability=prediction["predicted_probability"],
                    verified=False,
                )
                st.success("Quote saved.")

elif mode == "Model admin":
    st.header("Model admin")
    st.write("Train or retrain the model from quotes with known outcomes.")

    if st.button("Retrain model"):
        try:
            metrics = train_and_save_model()
            st.success("Model retrained successfully.")
            show_training_metrics(metrics)
        except Exception as e:
            st.error(str(e))
