import json
import logging
from pathlib import Path

import spacy

from src.reader import read_lusa

from ...constants import EXAMPLERS, RESOURCE_PATH, SAMPLE_DOCS_IDS


PWD = Path(__file__).parent

logger = logging.getLogger(__name__)


def annotate(language: str):
    corpus = read_lusa(RESOURCE_PATH / "lusa_news")

    docs2drop = SAMPLE_DOCS_IDS[language] + list(EXAMPLERS[language].values())
    test_docs = [doc for doc in corpus if doc.id not in docs2drop]

    predictions = []
    nlp = spacy.load("pt_core_news_sm")
    for doc in test_docs:

        participants = []
        ner = nlp(doc.text)
        for word in ner.ents:
            if word.label_ in ["PER", "ORG"]:
                participants.append(word.text)

        predictions.append({
            "model": "ner",
            "entity": "participants",
            "doc": doc.id,
            "entities": participants,
            "template": "-"
        })

    logger.info(f"Saving results.")
    outputpath = PWD / f"predictions_pt.json"
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
