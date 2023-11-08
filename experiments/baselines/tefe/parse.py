"""Run the best prompt for each model/entity pair on the test set."""

import json
import logging
from pathlib import Path

from ...constants import RESULTS_PATH


PWD = Path(__file__).parent

logger = logging.getLogger(__name__)


def _get_predictions():
    predictions = []
    annt_path = Path(__file__).parent / "annt"
    filepaths = annt_path.glob("*.json")
    for filepath in filepaths:
        doc = filepath.stem

        events = []
        annts = json.loads(filepath.read_text())
        for annt_str in annts:
            annt = json.loads(annt_str)
            if annt:
                for trigger in annt:
                    text = trigger["trigger"]["text"]
                    events.append(text)

        predictions.append({
            "model": "tefe",
            "entity": "event triggers",
            "doc": doc,
            "entities": events,
            "template": "-"
        })

    return predictions


def main():

    logger.info(f"Saving results.")
    filepath = PWD /  "predictions.json"
    if filepath.exists():
        content = json.load(filepath.open())
    else:
        content = []

    predictions = _get_predictions()
    
    json.dump(
        content + predictions,
        filepath.open("w"),
        ensure_ascii=False,
        indent=4
    )


if __name__ == "__main__":
    main()
