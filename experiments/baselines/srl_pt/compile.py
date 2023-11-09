import json
from pathlib import Path

PWD = Path(__file__).parent


def main():
    predictions = []
    for filepath in (PWD / "predictions").glob("*.json"):
        content = json.load(filepath.open())
        predictions.append(content)

    json.dump(
        predictions,
        (PWD / "predictions_pt.json").open("w"),
        indent=4,
        ensure_ascii=True
    )


if __name__ == "__main__":
    main()
