"""Select the best template for each model/entity pair on the test set."""

import logging
import os
import time

import dotenv
import openai
import fire

from src.prompts import Prompter
from src.reader import read_lusa, read_timebank

from utils import mid2model
from constants import (
    ENTITIES,
    EXAMPLERS,
    RESOURCE_PATH,
    ROOT,
    SAMPLE_DOCS_IDS
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RESULTS_PATH = ROOT / "results" / "prompt_selection"

dotenv.load_dotenv(ROOT / ".env")
openai.api_key = os.getenv("OPENAI_API_KEY")


def main(mid: str = "gpt4", language: str = "english"):
    model = mid2model(mid)
    entities = ENTITIES[language]
    sample_docs = SAMPLE_DOCS_IDS[language]
    examples = EXAMPLERS[language]
    if language == "portuguese":
        dataset = read_lusa(RESOURCE_PATH / "lusa_news")
    elif language == "english":
        dataset = read_timebank(RESOURCE_PATH / "timebank")

    docs = [doc for doc in dataset if doc.id in sample_docs]
    tids = ["cls", "cls_def", "cls_def_exp", "cls_exp", "ext", "ext_def", "ext_def_exp", "ext_exp"]

    n_iter = len(entities) * len(docs) * len(tids)
    iter = 0
    for entity in entities:
        logger.info(f"Entity: {entity}")

        example_doc_id = examples[entity]
        example = [doc for doc in dataset if doc.id == example_doc_id][0]

        for tid in tids:
            logger.info(f"Template: {tid}")

            task = "classification" if "cls" in tid else "extraction"
            example = example if "exp" in tid else None
            definition = "def" in tid

            prompter = Prompter(
                entity=entity,
                task=task,
                example=example,
                definition=definition,
            )

            for doc in docs:
                logger.info(f"Iteration {iter}/{n_iter}")

                prompt = prompter.generate(doc)
            
                answer_path = RESULTS_PATH / language / mid / entity / tid / f"{doc.id}.txt"
                if not answer_path.exists():
                    answer_path.parent.mkdir(parents=True, exist_ok=True)
                    answer = model(prompt)
                    answer_path.write_text(answer)
                    logger.info(f"{mid} Answer:\n{answer}")
                    time.sleep(10)
                else:
                    logger.info(f"{mid} answer already exists.")

                iter += 1


if __name__ == "__main__":
    fire.Fire(main)
