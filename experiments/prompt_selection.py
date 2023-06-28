"""Select the best template for each model/entity pair on the test set."""

import logging
import os

import dotenv
import openai
from constants import (
    ENTITIES,
    EXAMPLERS,
    MODELS,
    RESOURCE_PATH,
    ROOT,
    SAMPLE_DOCS_IDS
)

from src.prompts import TEMPLATES, Prompter
from src.reader import read_lusa

RESULTS_PATH = ROOT / "results" / "prompt_selection"

dotenv.load_dotenv(ROOT / ".env")
openai.api_key = os.getenv("OPENAI_API_KEY")


if __name__ == "__main__":

    lusa = read_lusa(RESOURCE_PATH / "lusa")

    docs = [doc for doc in lusa if doc.id in SAMPLE_DOCS_IDS]

    n_iter = len(ENTITIES) * len(docs) * len(TEMPLATES) * 2
    iter = 0
    for entity in ENTITIES:
        logging.info(f"\n\nEntity: {entity}")

        example_doc_id = EXAMPLERS[entity]
        example = [doc for doc in lusa if doc.id == example_doc_id][0]

        for tid, template in TEMPLATES.items():
            logging.info(f"\n\nTemplate: {tid}")

            task = "classification" if "cls" in tid else "extraction"

            prompter = Prompter(
                template=template,
                entity=entity,
                task=task,
                example=example
            )

            for doc in docs:
                logging.info(f"\n\nIteration {iter}/{n_iter}")

                prompt = prompter.generate(doc)

                for mid, model in MODELS.items():
                    prompt = prompter.generate(doc)

                    answer_path = RESULTS_PATH / "testset" / mid / \
                        entity / tid / f"{doc.id}.txt"
                    if not answer_path.exists():
                        answer_path.parent.mkdir(parents=True, exist_ok=True)
                        answer = model(prompt)
                        answer_path.write_text(answer)
                        logging.info(f"{mid} Answer:\n{answer}")
                    else:
                        logging.info("ChatGPT answer already exists.")

                    iter += 1
