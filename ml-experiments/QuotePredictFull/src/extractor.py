from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Union
import re

import fitz  # PyMuPDF

INDUSTRIES = [
    "Manufacturing",
    "Energy",
    "Construction",
    "Healthcare",
    "Retail",
    "Technology",
    "Public Sector",
]

RISK_PATTERNS = [
    r"unlimited liability",
    r"penalty clause",
    r"liquidated damages",
    r"termination for convenience",
    r"exclusive jurisdiction",
    r"non-standard warranty",
    r"late delivery penalty",
]


def extract_text_from_pdf(pdf_input: Union[str, Path, bytes]) -> str:
    """Extract full text from a PDF path or raw bytes."""
    if isinstance(pdf_input, (str, Path)):
        doc = fitz.open(pdf_input)
    else:
        doc = fitz.open(stream=pdf_input, filetype="pdf")

    pages = []
    for page in doc:
        pages.append(page.get_text("text", sort=True))

    doc.close()
    return "\n".join(pages)


def _normalize_amount(raw: str) -> Optional[float]:
    if not raw:
        return None

    value = raw.strip().replace(" ", "")

    if "," in value and "." in value:
        if value.rfind(",") > value.rfind("."):
            value = value.replace(".", "").replace(",", ".")
        else:
            value = value.replace(",", "")
    elif "," in value:
        parts = value.split(",")
        if len(parts[-1]) in (1, 2):
            value = value.replace(",", ".")
        else:
            value = value.replace(",", "")

    try:
        return float(value)
    except ValueError:
        return None


def extract_total_price(text: str) -> Optional[float]:
    patterns = [
        r"total\s+price\s*[:\-]?\s*(?:SEK|EUR|USD)?\s*([\d\s\.,]+)",
        r"grand\s+total\s*[:\-]?\s*(?:SEK|EUR|USD)?\s*([\d\s\.,]+)",
        r"contract\s+value\s*[:\-]?\s*(?:SEK|EUR|USD)?\s*([\d\s\.,]+)",
        r"quote\s+value\s*[:\-]?\s*(?:SEK|EUR|USD)?\s*([\d\s\.,]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return _normalize_amount(match.group(1))
    return None


def extract_delivery_time(text: str) -> Optional[int]:
    patterns = [
        r"delivery\s+time\s*[:\-]?\s*(\d+)\s*(day|days|week|weeks)",
        r"lead\s+time\s*[:\-]?\s*(\d+)\s*(day|days|week|weeks)",
        r"delivery\s+within\s*(\d+)\s*(day|days|week|weeks)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            amount = int(match.group(1))
            unit = match.group(2).lower()
            return amount * 7 if "week" in unit else amount
    return None


def extract_industry(text: str) -> str:
    labeled = re.search(r"industry\s*[:\-]?\s*([A-Za-z\s&]+)", text, flags=re.IGNORECASE)
    if labeled:
        candidate = labeled.group(1).strip().lower()
        for industry in INDUSTRIES:
            if industry.lower() in candidate:
                return industry

    keyword_map = {
        "Manufacturing": ["factory", "manufacturing", "production line"],
        "Energy": ["energy", "power plant", "grid", "substation"],
        "Construction": ["construction", "infrastructure", "building site"],
        "Healthcare": ["hospital", "healthcare", "medical", "clinic"],
        "Retail": ["retail", "store", "e-commerce"],
        "Technology": ["software", "technology", "cloud", "platform", "saas"],
        "Public Sector": ["municipality", "public sector", "government", "authority"],
    }

    lower_text = text.lower()
    for industry, keywords in keyword_map.items():
        if any(keyword in lower_text for keyword in keywords):
            return industry

    return "Unknown"


def extract_risk_clauses(text: str) -> int:
    lower_text = text.lower()
    return sum(1 for pattern in RISK_PATTERNS if re.search(pattern, lower_text))


def extract_keys_from_text(text: str) -> Dict[str, Union[str, int, float, None]]:
    return {
        "TotalPrice": extract_total_price(text),
        "DeliveryTime": extract_delivery_time(text),
        "Industry": extract_industry(text),
        "RiskClauses": extract_risk_clauses(text),
    }


def extract_quote_features(pdf_input: Union[str, Path, bytes]) -> Dict[str, Union[str, int, float, None]]:
    text = extract_text_from_pdf(pdf_input)
    return extract_keys_from_text(text)
