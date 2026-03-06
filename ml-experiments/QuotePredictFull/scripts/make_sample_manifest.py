from __future__ import annotations

from pathlib import Path
import pandas as pd


def main() -> None:
    sample = pd.DataFrame(
        [
            {"filename": "sample_quote_win.pdf", "Won_Quote": 1},
            {"filename": "sample_quote_loss.pdf", "Won_Quote": 0},
        ]
    )

    output = Path(__file__).resolve().parents[1] / "data" / "sample_manifest.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(output, index=False)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
