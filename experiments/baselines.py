"""Run the best prompt for each model/entity pair on the test set."""

import json

import spacy
from constants import EXAMPLERS, RESOURCE_PATH, ROOT, SAMPLE_DOCS_IDS
from py_heideltime import heideltime as heideltime_model

from src.reader import read_lusa

RESULTS_PATH = ROOT / "results" / "baselines"


def tei2go(docs):
    """Baseline that extracts the first sentence of the document."""

    nlp = spacy.load("pt_tei2go")

    results = []
    for doc in docs:
        text = nlp(doc.text)
        timexs = [ent.text for ent in text.ents]
        results.append({
            "model": "tei2go",
            "entity": "time expressions",
            "doc": doc.id,
            "entities": timexs,
            "template": "-"
        })

    return results


def heideltime(docs):
    """Baseline that extracts the first sentence of the document."""

    results = []
    for doc in docs:
        timexs = heideltime_model(doc.text, language='Portuguese', document_type='news')
        timexs = [timex["text"] for timex in timexs]
        results.append({
            "model": "tei2go",
            "entity": "time expressions",
            "doc": doc.id,
            "entities": timexs,
            "template": "-"
        })

    return results


def main():
    """Main script."""
    lusa = read_lusa(RESOURCE_PATH / "lusa")

    docs2drop = SAMPLE_DOCS_IDS + list(EXAMPLERS.values())
    test_docs = [doc for doc in lusa if doc.id not in docs2drop]

    heideltime_results = heideltime(test_docs)
    heideltime_result_filepath = RESULTS_PATH / "heideltime" / "predictions.json"
    heideltime_result_filepath.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        heideltime_results,
        heideltime_result_filepath.open("w"),
        ensure_ascii=False,
        indent=4
    )

    tei2go_results = tei2go(test_docs)
    tei2go_result_filepath = RESULTS_PATH / "tei2go" / "predictions.json"
    tei2go_result_filepath.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        tei2go_results,
        tei2go_result_filepath.open("w"),
        ensure_ascii=False,
        indent=4
    )


if __name__ == "__main__":
    main()
