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
    MODELS,
    RESOURCE_PATH,
    ROOT,
    SAMPLE_DOCS_IDS
)

from src.prompts import Prompter
from src.reader import read_lusa

logging.basicConfig(level=logging.INFO)

dotenv.load_dotenv(ROOT / ".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

RESULTS_PATH = ROOT / "results" / "test"


def main(mid: str = "chatgpt"):
    """Main script."""

    model = MODELS[mid]
    lusa = read_lusa(RESOURCE_PATH / "lusa_news")

    docs2drop = SAMPLE_DOCS_IDS + list(EXAMPLERS.values())
    test_docs = [doc for doc in lusa if doc.id not in docs2drop]

    n_iter = len(ENTITIES) * len(test_docs)
    iter = 0
    for entity in ENTITIES:
        logging.info(f"Entity: {entity}")

        example_doc_id = EXAMPLERS[entity]
        example = [doc for doc in lusa if doc.id == example_doc_id][0]

        tid = BEST_TEMPLATES[(mid, entity)]   
        task = "classification" if "cls" in tid else "extraction"
        example = example if "exp" in tid else None
        definition = "def" in tid
        prompter = Prompter(
            entity=entity,
            task=task,
            example=example,
            definition=definition,
        )

        for doc in test_docs:
            logging.info(f"Iteration {iter}/{n_iter}")

            prompt = prompter.generate(doc)

            answer_path = RESULTS_PATH / mid / entity / tid / f"{doc.id}.txt"
            if not answer_path.exists():
                answer_path.parent.mkdir(parents=True, exist_ok=True)
                answer = model(prompt)
                answer_path.write_text(answer)
                logging.info(f"{mid} Answer:\n{answer}")

                time.sleep(5)

            else:
                logging.info(f"{mid} answer already exists.")

            iter += 1


if __name__ == "__main__":
    fire.Fire(main)
