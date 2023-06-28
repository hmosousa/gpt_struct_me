
from pathlib import Path

from src.models import chatgpt, gpt3


ROOT = Path(__file__).parent.parent
RESOURCE_PATH = ROOT / "resources"
RESULTS_PATH = ROOT / "results"


SAMPLE_DOCS_IDS = [
    "lusa_190",
    "lusa_101",
    "lusa_178",
    "lusa_162",
    "lusa_161",
    "lusa_177",
    "lusa_196",
    "lusa_174",
    "lusa_166",
    "lusa_13",
    "lusa_124",
    "lusa_140",
    "lusa_189",
    "lusa_168",
    "lusa_149",
    "lusa_192",
    "lusa_132",
    "lusa_10",
    "lusa_115",
    "lusa_199",
]

EXAMPLERS = {
    "event triggers": "lusa_181",
    "time expressions": "lusa_11",
    "participants": "lusa_157"
}

ENTITIES = [
    "event triggers",
    "participants",
    "time expressions",
]


BEST_FEW_SHOT_TEMPLATES = {
    ("gpt3", "event triggers"): "ext_def_exp",
    ("gpt3", "participants"): "cls_exp",
    ("gpt3", "time expressions"): "ext_exp",
    ("chatgpt", "event triggers"): "ext_def_exp",
    ("chatgpt", "participants"): "ext_def_exp",
    ("chatgpt", "time expressions"): "cls_def_exp",
}


BEST_ZERO_SHOT_TEMPLATES = {
    ("gpt3", "event triggers"): "cls_def",
    ("gpt3", "participants"): "cls",
    ("gpt3", "time expressions"): "ext",
    ("chatgpt", "event triggers"): "cls_def",
    ("chatgpt", "participants"): "cls",
    ("chatgpt", "time expressions"): "ext",
}


MODELS = {
    "gpt3": gpt3,
    "chatgpt": chatgpt
}
