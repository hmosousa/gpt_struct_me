
import gc
import re
import json
from pathlib import Path

from allennlp.models.archival import load_archive
from allennlp.predictors.predictor import Predictor

from my_predict import predictManager


PWD = Path(__file__).resolve().parent


def annt(inputpath):
    model = PWD / "srl-enpt_xlmr-large"
    outputpath = Path("output.txt")

    outputpath.unlink(missing_ok=True)

    archive = load_archive(model)

    predictor = Predictor.from_archive(archive, "my_predictor", dataset_reader_to_load="train")

    manager = predictManager(predictor, inputpath, None, 1, False, False)
    manager.run()

    result = json.load(outputpath.open("r", encoding="utf-8"))
    outputpath.unlink(missing_ok=True)

    return result


def get_timexs(results):
    timexs = []
    for result in results:
        if isinstance(result, dict):
            for verb in result["verbs"]:
                timex = []
                for word, tag in zip(result["words"], verb["tags"]):
                    if "TMP" in tag:
                        timex.append(word)

                    if "TMP" not in tag and timex:
                        timexs.append(" ".join(timex))
                        timex = []
    if timex:
        timexs.append(" ".join(timex))

    return timexs


def get_events(results):
    events = []
    for result in results:
        if isinstance(result, dict):
            for verb in result["verbs"]:
                events.append(verb["verb"])
    return events


def get_participants(results):
    arg_re = re.compile(r"\[A[\dM]+-*(\w*): (.*?)\]")
    participants = []
    arguments = []
    for result in results:
        if isinstance(result, dict):
            for verb in result["verbs"]:
                arguments += arg_re.findall(verb["description"])

    for tag, arg in arguments:
        if tag in ["DIS", ""]:
            participants.append(arg)

    return participants


def main():
    filepaths = (PWD / "tmp").glob("*.txt")
    outputdir = PWD / "predictions"
    outputdir.mkdir(exist_ok=True)
    for filepath in filepaths:
        results = annt(filepath)

        participants = get_participants(results)
        json.dump({
            "model": "srl",
            "entity": "participants",
            "doc": filepath.stem,
            "entities": participants,
            "template": "-"
        },
            (outputdir / f"{filepath.stem}_part.json").open("w"),
            ensure_ascii=True,
            indent=4
        )
        gc.collect()

        timexs = get_timexs(results)
        json.dump({
            "model": "srl",
            "entity": "time expressions",
            "doc": filepath.stem,
            "entities": timexs,
            "template": "-"
        },
            (outputdir / f"{filepath.stem}_timex.json").open("w"),
            ensure_ascii=True,
            indent=4
        )
        gc.collect()

        events = get_events(results)
        json.dump({
            "model": "srl",
            "entity": "event triggers",
            "doc": filepath.stem,
            "entities": events,
            "template": "-"
        },
            (outputdir / f"{filepath.stem}_event.json").open("w"),
            ensure_ascii=True,
            indent=4
        )
        gc.collect()


if __name__ == "__main__":
    main()
