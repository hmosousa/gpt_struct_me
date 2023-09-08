
from pathlib import Path

from src.models import chatgpt, gpt3, gpt4


ROOT = Path(__file__).parent.parent
RESOURCE_PATH = ROOT / "resources"
RESULTS_PATH = ROOT / "results"


SAMPLE_DOCS_IDS = [
    "lusa_189",
    "lusa_100",
    "lusa_197",
    "lusa_161",
    "lusa_116",
    "lusa_176",
    "lusa_195",
    "lusa_173",
    "lusa_172",
    "lusa_13",
    "lusa_142",
    "lusa_126",
    "lusa_188",
    "lusa_107",
    "lusa_203",
    "lusa_191",
    "lusa_170",
    "lusa_133",
    "lusa_179",
    "lusa_155",
]

EXAMPLERS = {
    "event triggers": "lusa_119",
    "time expressions": "lusa_11",
    "participants": "lusa_156"
}

ENTITIES = [
    "event triggers",
    "participants",
    "time expressions",
]

BEST_TEMPLATES = {
    ("chatgpt", "event triggers"): "cls_def_exp",
    ("chatgpt", "participants"): "cls_def",
    ("chatgpt", "time expressions"): "ext",

    ("gpt3", "event triggers"): "cls_def_exp",
    ("gpt3", "participants"): "cls",
    ("gpt3", "time expressions"): "ext_exp",
    
    ("gpt4", "event triggers"): "cls_exp",
    ("gpt4", "participants"): "cls_def",
    ("gpt4", "time expressions"): "cls",
}

MODELS = {
    "gpt3": gpt3,
    "chatgpt": chatgpt,
    "gpt4": gpt4,
}
