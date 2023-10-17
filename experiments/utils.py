
from src.models import (
    chatgpt,
    gpt3,
    gpt4,
    Falcon,
    Llama2InferenceAPI,
    HFInferenceLocal,
    llama2_70b
)


def mid2model(mid: str):
    if mid == "gpt3":
        return gpt3

    elif mid == "chatgpt":
        return chatgpt

    elif mid == "gpt4":
        return gpt4

    elif mid == "falcon-7b":
        return Falcon("7b", instruct=False)

    elif mid == "falcon-7b-instruct":
        return Falcon("7b", instruct=True)

    elif mid == "falcon-40b":
        return HFInferenceLocal()

    elif mid == "falcon-40b-instruct":
        return Falcon("40b", instruct=True)

    elif mid == "llama2-7b":
        return Llama2InferenceAPI("7b", chat=False)

    elif mid == "llama2-13b":
        return Llama2InferenceAPI("13b", chat=False)

    elif mid == "llama2-70b":
        return llama2_70b

    elif mid == "llama2-7b-chat":
        return Llama2InferenceAPI("7b", chat=True)

    elif mid == "llama2-13b-chat":
        return Llama2InferenceAPI("13b", chat=True)

    elif mid == "llama2-70b-chat":
        return Llama2InferenceAPI("70b", chat=True)
