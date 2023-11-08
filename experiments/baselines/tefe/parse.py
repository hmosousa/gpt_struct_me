"""Run the best prompt for each model/entity pair on the test set."""

import json
import logging
from pathlib import Path

from ...constants import RESULTS_PATH


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
    result_filepath_pt = RESULTS_PATH / "test" / "portuguese" / "predictions.json"
    if result_filepath_pt.exists():
        content = json.load(result_filepath_pt.open())
    else:
        content = []

    predictions = _get_predictions()
    
    json.dump(
        content + predictions,
        result_filepath_pt.open("w"),
        ensure_ascii=False,
        indent=4
    )


if __name__ == "__main__":
    main()
