"""Run the best prompt for each model/entity pair on the test set."""

import json
import logging
from pathlib import Path

import spacy

from src.reader import read_lusa, read_timebank

from ...constants import EXAMPLERS, RESOURCE_PATH, RESULTS_PATH, SAMPLE_DOCS_IDS


PWD = Path(__file__).parent 

logger = logging.getLogger(__name__)


def tei2go(docs, language: str):
    """Baseline that extracts the first sentence of the document."""

    if language == "portuguese":
        nlp = spacy.load("pt_tei2go")
    elif language == "english":
        nlp = spacy.load("en_tei2go")
    else:
        raise ValueError(f"Language {language} not supported.")

    predictions = []
    for doc in docs:
        text = nlp(doc.text)
        timexs = [ent.text for ent in text.ents]
        predictions.append({
            "model": "tei2go",
            "entity": "time expressions",
            "doc": doc.id,
            "entities": timexs,
            "template": "-"
        })

    return predictions


def annotate(language: str):
    if language == "portuguese":
        corpus = read_lusa(RESOURCE_PATH / "lusa_news")
        lang = "pt"
    elif language == "english":
        corpus = read_timebank(RESOURCE_PATH / "timebank")
        lang = "en"

    docs2drop = SAMPLE_DOCS_IDS[language] + list(EXAMPLERS[language].values())
    test_docs = [doc for doc in corpus if doc.id not in docs2drop]

    predictions = tei2go(test_docs, language)

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
