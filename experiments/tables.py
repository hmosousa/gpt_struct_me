import json

import pandas as pd

from constants import ROOT, ENTITIES, MODELS

RESULTS_PATH = ROOT / "results" / "test"


def main():
    """Main script."""
    content = (RESULTS_PATH / "results.json").read_text()
    results = json.loads(content)

    for result in results:
        strict = result.pop("strict")
        result["precision"] = strict["precision"]
        result["recall"] = strict["recall"]
        result["f1"] = strict["f1"]

        relaxed = result.pop("relaxed")
        result["f1_r"] = relaxed["f1"]

    df = pd.DataFrame(results)
    for entity in ENTITIES:
        df_entity = df[df.entity == entity]
        df_entity.drop("entity", axis=1, inplace=True)
        for model in MODELS:
            df_model = df_entity[df_entity.model == model]
            df_model.drop("model", axis=1, inplace=True)
            df_model.sort_values(by=["template"], ascending=True, inplace=True)
            df_model.to_csv(f"{model}_{entity}.csv", index=False)


if __name__ == "__main__":
    main()
