from __future__ import annotations

from pathlib import Path
import fitz


def render_first_page_as_png(pdf_path: str | Path, zoom: float = 1.5) -> bytes:
    doc = fitz.open(pdf_path)
    page = doc[0]
    matrix = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=matrix)
    png_bytes = pix.tobytes("png")
    doc.close()
    return png_bytes
