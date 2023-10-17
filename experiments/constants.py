from pathlib import Path


ROOT = Path(__file__).parent.parent
RESOURCE_PATH = ROOT / "resources"
RESULTS_PATH = ROOT / "results"


SAMPLE_DOCS_IDS = {
    "portuguese": [
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
    ],

    "english": [
        "wsj_0551",
        "wsj_0815",
        "wsj_0135",
        "wsj_1042",
        "wsj_0266",
        "wsj_0924",
        "PRI19980306.2000.1675",
        "wsj_0332",
        "wsj_0176",
        "wsj_0348",
        "wsj_0144",
        "wsj_0670",
        "ABC19980114.1830.0611",
        "wsj_0674",
        "wsj_0376",
        "VOA19980305.1800.2603",
        "APW19980301.0720",
        "wsj_0938",
        "wsj_0745",
        "wsj_0584",
    ]
}
EXAMPLERS = {
    "portuguese": {
        "event triggers": "lusa_119",
        "time expressions": "lusa_11",
        "participants": "lusa_156"
    },
    "english": {
        "event triggers": "APW19980213.1310",
        "time expressions": "APW19980306.1001",
    }
}

ENTITIES = {
    "portuguese": [
        "event triggers",
        "participants",
        "time expressions",
    ],
    "english": [
        "event triggers",
        "time expressions",
    ]
}

BEST_TEMPLATES = {
    "portuguese": {
        ("chatgpt", "event triggers"): "ext_def_exp",
        ("chatgpt", "participants"): "ext_def_exp",
        ("chatgpt", "time expressions"): "ext",

        ("gpt3", "event triggers"): "ext_exp",
        ("gpt3", "participants"): "cls_exp",
        ("gpt3", "time expressions"): "ext_exp",

        ("gpt4", "event triggers"): "ext_def_exp",
        ("gpt4", "participants"): "ext_def_exp",
        ("gpt4", "time expressions"): "ext_exp",

        ("llama2-13b", "event triggers"): "ext_def_exp",
        ("llama2-13b", "participants"): "ext_exp",
        ("llama2-13b", "time expressions"): "ext",

        ("llama2-13b-chat", "event triggers"): "cls_def_exp",
        ("llama2-13b-chat", "participants"): "cls_exp",
        ("llama2-13b-chat", "time expressions"): "ext",

        ("llama2-70b", "event triggers"): "ext_exp",
        ("llama2-70b", "participants"): "ext_def_exp",
        ("llama2-70b", "time expressions"): "ext_exp",

        ("llama2-70b-chat", "event triggers"): "cls_def_exp",
        ("llama2-70b-chat", "participants"): "ext_def_exp",
        ("llama2-70b-chat", "time expressions"): "ext_exp",

        ("llama2-7b", "event triggers"): "ext_exp",
        ("llama2-7b", "participants"): "cls_def_exp",
        ("llama2-7b", "time expressions"): "cls_exp",

        ("llama2-7b-chat", "event triggers"): "cls_exp",
        ("llama2-7b-chat", "participants"): "cls_def_exp",
        ("llama2-7b-chat", "time expressions"): "cls_def_exp",
    },

    "english": {
        ("chatgpt", "event triggers"): "cls_def_exp",
        ("chatgpt", "time expressions"): "ext_def_exp",

        ("gpt3", "event triggers"): "ext_def_exp",
        ("gpt3", "time expressions"): "ext_def_exp",

        ("gpt4", "event triggers"): "cls_def_exp",
        ("gpt4", "time expressions"): "cls_def",

        ("llama2-13b", "event triggers"): "ext_def_exp",
        ("llama2-13b", "time expressions"): "ext_def",

        ("llama2-13b-chat", "event triggers"): "ext_exp",
        ("llama2-13b-chat", "time expressions"): "ext_def",

        ("llama2-70b", "event triggers"): "ext_exp",
        ("llama2-70b", "time expressions"): "ext_exp",

        ("llama2-70b-chat", "event triggers"): "ext_def_exp",
        ("llama2-70b-chat", "time expressions"): "ext",

        ("llama2-7b", "event triggers"): "ext_def_exp",
        ("llama2-7b", "time expressions"): "ext_def_exp",

        ("llama2-7b-chat", "event triggers"): "ext_def_exp",
        ("llama2-7b-chat", "time expressions"): "ext_def",
    }
}
