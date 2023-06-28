"""Parse models predictions."""

import json
from pathlib import Path

from constants import ROOT

RESULTS_PATH = ROOT / "results" / "test"


def read_json(filepath: Path) -> dict:
    """Read a JSON file."""
    content = filepath.read_text()
    try:
        answer = json.loads(content)
        return answer

    except json.decoder.JSONDecodeError:
        print(filepath)
        return []


def read_predictions():
    """Parse the prediction files."""
    predictions = []
    filepaths = RESULTS_PATH.glob("**/*.txt")
    for filepath in filepaths:
        *_, model, entity, template, _ = filepath.parts
        doc = filepath.stem

        answer = read_json(filepath)
        if "ext" in template:
            predictions.append({
                "model": model,
                "entity": entity,
                "doc": doc,
                "template": template,
                "answer": answer,
                "entities": answer
            })

        else:
            entities, classes = list(zip(*answer)) if answer else ([], [])
            predictions.append({
                "model": model,
                "entity": entity,
                "doc": doc,
                "template": template,
                "answer": answer,
                "entities": entities,
                "classes": classes
            })

    return predictions


def main() -> None:
    """Run the script."""
    predictions = read_predictions()

    predictions_path = RESULTS_PATH / "predictions.json"
    json.dump(predictions, predictions_path.open("w"), indent=4)


if __name__ == "__main__":
    main()
