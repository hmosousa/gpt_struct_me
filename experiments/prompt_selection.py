"""Select the best template for each model/entity pair on the test set."""

import logging
import os
import time

import dotenv
import openai
import fire
from constants import (
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

RESULTS_PATH = ROOT / "results" / "prompt_selection"

dotenv.load_dotenv(ROOT / ".env")
openai.api_key = os.getenv("OPENAI_API_KEY")


def main(mid: str = "gpt4"):
    model = MODELS[mid]

    lusa = read_lusa(RESOURCE_PATH / "lusa_news")

    docs = [doc for doc in lusa if doc.id in SAMPLE_DOCS_IDS]
    tids = ["cls", "cls_def", "cls_def_exp", "cls_exp", "ext", "ext_def", "ext_def_exp", "ext_exp"]

    n_iter = len(ENTITIES) * len(docs) * len(tids)
    iter = 0
    for entity in ENTITIES:
        logging.info(f"Entity: {entity}")

        example_doc_id = EXAMPLERS[entity]
        example = [doc for doc in lusa if doc.id == example_doc_id][0]

        for tid in tids:
            logging.info(f"Template: {tid}")

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
                logging.info(f"Iteration {iter}/{n_iter}")

                prompt = prompter.generate(doc)
            
                answer_path = RESULTS_PATH / mid / entity / tid / f"{doc.id}.txt"
                if not answer_path.exists():
                    answer_path.parent.mkdir(parents=True, exist_ok=True)
                    answer = model(prompt)
                    answer_path.write_text(answer)
                    logging.info(f"{mid} Answer:\n{answer}")
                    time.sleep(10)
                else:
                    logging.info(f"{mid} answer already exists.")

                iter += 1


if __name__ == "__main__":
    fire.Fire(main)
