"""Parse models predictions."""

import json
from pathlib import Path

import fire
import pandas as pd

from constants import RESOURCE_PATH, ROOT

from src.reader import read_lusa
from src.evaluate import strict_metrics, relaxed_metrics

RESULTS_PATH = ROOT / "results"


def read_predicions(path: Path) -> dict:
    """Read and structure the predictions of the models."""
    predictions_path = path / "predictions.json"
    content = json.loads(predictions_path.read_text())

    predictions = {}
    for prediction in content:
        model = prediction["model"]
        template = prediction["template"]
        doc = prediction["doc"]
        entity = prediction["entity"]
        pred = prediction["entities"]

        if model not in predictions:
            predictions[model] = {}
        if template not in predictions[model]:
            predictions[model][template] = {}
        if entity not in predictions[model][template]:
            predictions[model][template][entity] = {}
        if doc not in predictions[model][template][entity]:
            predictions[model][template][entity][doc] = []

        predictions[model][template][entity][doc] = pred
    return predictions


def read_annoations() -> dict:
    """Read and structure the annotations of the corpus."""
    lusa_path = RESOURCE_PATH / "lusa_news"
    documents = read_lusa(lusa_path)

    annotations = {}
    annotations["event triggers"] = {
        doc.id: [event.text for event in doc.events]
        for doc in documents
    }

    annotations["participants"] = {
        doc.id: [participant.text for participant in doc.participants]
        for doc in documents
    }

    annotations["time expressions"] = {
        doc.id: [timex.text for timex in doc.timexs]
        for doc in documents
    }

    return annotations


def evaluate(predicitons: dict, annotations: dict) -> list:
    """Evaluate the predictions of the models."""
    results = []
    for model, templates in predicitons.items():
        for template, entities in templates.items():
            for entity, prediction in entities.items():

                annotation = annotations[entity]
                strict = strict_metrics(prediction, annotation)
                relaxed = relaxed_metrics(prediction, annotation)
                results.append({
                    "model": model,
                    "template": template,
                    "entity": entity,
                    "strict": strict,
                    "relaxed": relaxed
                })
    return results


def make_results_table(results: list) -> pd.DataFrame:
    for result in results:
        strict = result.pop("strict")
        result["precision"] = strict["precision"]
        result["recall"] = strict["recall"]
        result["f1"] = strict["f1"]

        relaxed = result.pop("relaxed")
        result["f1_r"] = relaxed["f1"]
    df = pd.DataFrame(results)
    df.sort_values(["model", "entity", "f1"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df



def main(mode: str = "test", store_table: bool = True) -> None:
    path = RESULTS_PATH / mode
    predictions = read_predicions(path)
    annotations = read_annoations()

    results = evaluate(predictions, annotations)

    output_path = path / "results.json"
    json.dump(results, output_path.open("w"), indent=4)

    if store_table:
        table = make_results_table(results)
        print(table.to_string())
        table.to_csv(path / "results.csv", index=False)
        

if __name__ == "__main__":
    fire.Fire(main)
