"""Parse models predictions."""

import json
import logging
from pathlib import Path

import fire 

from constants import ROOT

logging.basicConfig(level=logging.INFO)

RESULTS_PATH = ROOT / "results"


def read_json(filepath: Path) -> dict:
    """Read a JSON file."""
    content = filepath.read_text()
    try:
        answer = json.loads(content)
        return answer

    except json.decoder.JSONDecodeError:
        logging.info(f"Wasn't able to parse {filepath}")
        print(filepath)
        return []


def read_predictions(path: Path):
    """Parse the prediction files."""
    predictions = []
    filepaths = path.glob("**/*.txt")
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


def main(mode: str = "prompt_selection") -> None:
    """Run the script."""
    path = RESULTS_PATH / mode

    predictions = read_predictions(path)

    predictions_path = path / "predictions.json"
    json.dump(predictions, predictions_path.open("w"), indent=4)


if __name__ == "__main__":
    fire.Fire(main)
