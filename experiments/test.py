"""Run the best prompt for each model/entity pair on the test set."""

import os
import time

import dotenv
import openai
from constants import (
    BEST_FEW_SHOT_TEMPLATES,
    BEST_ZERO_SHOT_TEMPLATES,
    ENTITIES,
    EXAMPLERS,
    MODELS,
    RESOURCE_PATH,
    ROOT,
    SAMPLE_DOCS_IDS
)

from src.prompts import TEMPLATES, Prompter
from src.reader import read_lusa

dotenv.load_dotenv(ROOT / ".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

RESULTS_PATH = ROOT / "results" / "test"


def main():
    """Main script."""
    lusa = read_lusa(RESOURCE_PATH / "lusa")

    docs2drop = SAMPLE_DOCS_IDS + list(EXAMPLERS.values())
    test_docs = [doc for doc in lusa if doc.id not in docs2drop]

    n_iter = len(ENTITIES) * len(test_docs) * len(MODELS)
    iter = 0
    for entity in ENTITIES:
        print(f"Entity: {entity}")

        example_doc_id = EXAMPLERS[entity]
        example = [doc for doc in lusa if doc.id == example_doc_id][0]

        for doc in test_docs:

            for mid, model in MODELS.items():

                tid = BEST_ZERO_SHOT_TEMPLATES[(mid, entity)]
                template = TEMPLATES[tid]

                task = "classification" if "cls" in tid else "extraction"
                prompter = Prompter(
                    template=template,
                    entity=entity,
                    task=task,
                    example=example
                )

                print(f"Iteration {iter}/{n_iter}")

                prompt = prompter.generate(doc)

                answer_path = RESULTS_PATH / mid / \
                    entity / tid / f"{doc.id}.txt"
                if not answer_path.exists():
                    answer_path.parent.mkdir(parents=True, exist_ok=True)
                    answer = model(prompt)
                    answer_path.write_text(answer)
                    print(f"{mid} Answer:\n{answer}")

                    time.sleep(5)

                else:
                    print(f"{mid} answer already exists.")

                iter += 1


if __name__ == "__main__":
    main()
