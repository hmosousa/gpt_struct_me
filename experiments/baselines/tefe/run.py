"""Run the best prompt for each model/entity pair on the test set."""

import logging
from pathlib import Path

from ...constants import (
    EXAMPLERS,
    RESOURCE_PATH,
    SAMPLE_DOCS_IDS
)

from src.reader import read_lusa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main script."""
    language = "portuguese"
    sample_docs = SAMPLE_DOCS_IDS[language]
    examples = EXAMPLERS[language]

    dataset = read_lusa(RESOURCE_PATH / "lusa_news")
    
    docs2drop = sample_docs + list(examples.values())
    test_docs = [doc for doc in dataset if doc.id not in docs2drop]

    tmp_path =  Path(__file__).parent / "tmp"
    tmp_path.mkdir(exist_ok=True)

    for doc in test_docs:
        filename = f"{doc.id}.txt"
        filepath = tmp_path / filename
        filepath.write_text(doc.text)


if __name__ == "__main__":
    main()
