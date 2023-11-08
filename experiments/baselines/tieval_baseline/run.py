"""Run the best prompt for each model/entity pair on the test set."""

import json
import logging

from tieval.models import EventIdentificationBaseline 

from src.reader import read_timebank

from ...constants import EXAMPLERS, RESOURCE_PATH, RESULTS_PATH, SAMPLE_DOCS_IDS


logger = logging.getLogger(__name__)


def _get_predictions(docs):
    """Baseline that extracts the first sentence of the document."""
    model = EventIdentificationBaseline()
    
    for doc in docs:
        doc.name = doc.id

    preds = model.predict(docs)

    predictions = []
    for doc_id, events in preds.items():
        entities = [ent.text for ent in events]
        predictions.append({
            "model": "tieval_baseline",
            "entity": "event triggers",
            "doc": doc_id,
            "entities": entities,
            "template": "-"
        })

    return predictions


def main():
    language = "english"
    corpus = read_timebank(RESOURCE_PATH / "timebank")

    docs2drop = SAMPLE_DOCS_IDS[language] + list(EXAMPLERS[language].values())
    test_docs = [doc for doc in corpus if doc.id not in docs2drop]

    predictions = _get_predictions(test_docs)

    logger.info(f"Saving results.")
    filepath = RESULTS_PATH / "test" / "english" / "predictions.json"
    if filepath.exists():
        content = json.load(filepath.open())
    else:
        content = []

    json.dump(
        content + predictions,
        filepath.open("w"),
        ensure_ascii=False,
        indent=4
    )


if __name__ == "__main__":
    main()
