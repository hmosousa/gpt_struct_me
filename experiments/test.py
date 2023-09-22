"""Run the best prompt for each model/entity pair on the test set."""

import os
import time
import logging

import fire
import dotenv
import openai
from constants import (
    BEST_TEMPLATES,
    ENTITIES,
    EXAMPLERS,
    RESOURCE_PATH,
    ROOT,
    SAMPLE_DOCS_IDS
)

from src.prompts import Prompter
from src.reader import read_lusa, read_timebank

from utils import mid2model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv(ROOT / ".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

RESULTS_PATH = ROOT / "results" / "test"


def main(mid: str = "chatgpt", language: str = "english"):
    """Main script."""
    model = mid2model(mid)
    entities = ENTITIES[language]
    sample_docs = SAMPLE_DOCS_IDS[language]
    examples = EXAMPLERS[language]
    best_templates = BEST_TEMPLATES[language]
    if language == "portuguese":
        dataset = read_lusa(RESOURCE_PATH / "lusa_news")
    elif language == "english":
        dataset = read_timebank(RESOURCE_PATH / "timebank")
    
    docs2drop = sample_docs + list(examples.values())
    test_docs = [doc for doc in dataset if doc.id not in docs2drop]

    n_iter = len(entities) * len(test_docs)
    iter = 0
    for entity in entities:
        logger.info(f"Entity: {entity}")

        tid = best_templates[(mid, entity)]   
        task = "classification" if "cls" in tid else "extraction"
        if "exp" in tid:
            example_doc_id = examples[entity]
            example = [doc for doc in dataset if doc.id == example_doc_id][0]
        else:
            example = None
        definition = "def" in tid
        prompter = Prompter(
            entity=entity,
            task=task,
            example=example,
            definition=definition,
        )

        for doc in test_docs:
            logger.info(f"Iteration {iter}/{n_iter}")

            prompt = prompter.generate(doc.text)

            answer_path = RESULTS_PATH / language / mid / entity / tid / f"{doc.id}.txt"
            if not answer_path.exists():
                answer_path.parent.mkdir(parents=True, exist_ok=True)
                answer = model(prompt)
                answer_path.write_text(answer)
                logger.info(f"{mid} Answer:\n{answer}")
                time.sleep(20)

            else:
                logger.info(f"{mid} answer already exists.")

            iter += 1


if __name__ == "__main__":
    fire.Fire(main)
