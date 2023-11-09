"""Run the best prompt for each model/entity pair on the test set."""

import json
import logging
from pathlib import Path

from py_heideltime import heideltime as heideltime_model

from src.reader import read_lusa, read_timebank

from ...constants import EXAMPLERS, RESOURCE_PATH, RESULTS_PATH, SAMPLE_DOCS_IDS


PWD = Path(__file__).parent 

logger = logging.getLogger(__name__)


def heideltime(docs, language: str):
    """Baseline that extracts the first sentence of the document."""

    if language == "portuguese":
        language = "Portuguese"
    elif language == "english":
        language = "English"
    else:
        raise ValueError(f"Language {language} not supported.")

    results = []
    for doc in docs:
        timexs = heideltime_model(doc.text, language=language, document_type='news')
        timexs = [timex["text"] for timex in timexs]
        results.append({
            "model": "heildeltime",
            "entity": "time expressions",
            "doc": doc.id,
            "entities": timexs,
            "template": "-"
        })

    return results


def annotate(language: str):
    if language == "portuguese":
        corpus = read_lusa(RESOURCE_PATH / "lusa_news")
        lang = "pt"
    elif language == "english":
        corpus = read_timebank(RESOURCE_PATH / "timebank")
        lang = "en"

    docs2drop = SAMPLE_DOCS_IDS[language] + list(EXAMPLERS[language].values())
    test_docs = [doc for doc in corpus if doc.id not in docs2drop]

    predictions = heideltime(test_docs, language)

    logger.info(f"Saving results.")
    outputpath = PWD / f"predictions_{lang}.json"
    json.dump(
        predictions,
        outputpath.open("w"),
        ensure_ascii=False,
        indent=4
    )


def main():
    """Main script."""
    annotate("portuguese")
    annotate("english")


if __name__ == "__main__":
    main()
