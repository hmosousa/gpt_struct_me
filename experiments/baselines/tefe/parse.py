import json
import logging
from pathlib import Path

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
    outputpath = PWD / "predictions_pt.json"

    predictions = _get_predictions()

    json.dump(
        predictions,
        outputpath.open("w"),
        ensure_ascii=False,
        indent=4
    )


if __name__ == "__main__":
    main()
