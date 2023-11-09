"""Compiles the predictions from all baselines and adds them to the predictions.json file in the 
results folder."""
import json
import logging
from pathlib import Path

PWD = Path(__file__).parent
RESULTS_PATH = PWD.parent.parent / "results"

logger = logging.getLogger(__name__)


def main():
    predictions_pt, predictions_en = [], []
    filepaths = PWD.glob("**/predictions*.json")
    for filepath in filepaths:
        content = json.load(filepath.open())
        if filepath.stem.endswith("_pt"):
            predictions_pt += content
        elif filepath.stem.endswith("_en"):
            predictions_en += content

    outputpath = RESULTS_PATH / "test" / "portuguese" / "predictions.json"
    if outputpath.exists():
        content = json.load(outputpath.open())
    else:
        content = []

    json.dump(
        content + predictions_pt,
        outputpath.open("w"),
        indent=4,
        ensure_ascii=True
    )

    outputpath = RESULTS_PATH / "test" / "english" / "predictions.json"
    if outputpath.exists():
        content = json.load(outputpath.open())
    else:
        content = []

    json.dump(
        content + predictions_en,
        outputpath.open("w"),
        indent=4,
        ensure_ascii=True
    )


if __name__ == "__main__":
    main()
