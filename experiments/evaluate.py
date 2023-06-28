"""Parse models predictions."""

import json

from constants import RESOURCE_PATH, ROOT

from src.reader import read_lusa
from src.evaluate import strict_metrics, relaxed_metrics

RESULTS_PATH = ROOT / "results" / "test"


def read_predicions() -> dict:
    """Read and structure the predictions of the models."""
    predictions_path = RESULTS_PATH / "predictions.json"
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
    lusa_path = RESOURCE_PATH / "lusa"
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


if __name__ == "__main__":

    annotations = read_annoations()
    predictions = read_predicions()

    results = evaluate(predictions, annotations)

    output_path = RESULTS_PATH / "results.json"
    json.dump(results, output_path.open("w"), indent=4)
