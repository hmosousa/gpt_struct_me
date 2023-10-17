"""Parse models predictions."""

import json
import logging
from pathlib import Path

import fire
from src.utils import is_json

from constants import ROOT

logging.basicConfig(level=logging.INFO)

RESULTS_PATH = ROOT / "results"


def json_loads_section(content: str) -> dict:
    """Parse a section of a JSON file."""
    content = content.strip()
    lines = content.split("\n")
    running_content = ""
    while lines:
        running_content += lines.pop(0)
        if is_json(running_content):
            return json.loads(running_content)
    raise ValueError("Invalid JSON")


def read_json(filepath: Path) -> dict:
    """Read a JSON file."""
    content = filepath.read_text()
    try:
        answer = json.loads(content)
        return answer

    except json.decoder.JSONDecodeError:
        try:
            answer = json_loads_section(content)
            return answer
        
        except ValueError:
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
            is_valid = len(answer) and isinstance(answer, list) and isinstance(answer[0], str)
            if not is_valid:
                answer = []

            predictions.append({
                "model": model,
                "entity": entity,
                "doc": doc,
                "template": template,
                "answer": answer,
                "entities": answer
            })

        else:
            is_valid = isinstance(answer, list) and \
                all(isinstance(a, list) for a in answer) and \
                all(len(a) == 2 for a in answer) and \
                all(isinstance(a[0], str) for a in answer)
                
            if not is_valid:
                answer = []

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


def main(mode: str = "prompt_selection", language: str = "portuguese") -> None:
    """Run the script."""
    path = RESULTS_PATH / mode / language

    predictions = read_predictions(path)

    predictions_path = path / "predictions.json"
    json.dump(predictions, predictions_path.open("w"), indent=4)


if __name__ == "__main__":
    fire.Fire(main)
