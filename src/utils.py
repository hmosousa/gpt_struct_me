"""Utility functions for the project."""

import json
import re


def is_sublist(list1: list, list2: list) -> bool:
    """Check if list1 is a subset of list2."""
    if len(list1) > len(list2):
        return False

    for i in range(len(list2) - len(list1) + 1):
        if list2[i:i + len(list1)] == list1:
            return True
    return False


def string_overlap(source: str, target: str) -> bool:
    """Check if two strings overlap at the word level."""
    if source == "" or target == "":
        return False

    tkns_src = tokenize(source)
    tkns_tgt = tokenize(target)

    src_in_tgt = is_sublist(tkns_src, tkns_tgt)
    tgt_in_src = is_sublist(tkns_tgt, tkns_src)
    if src_in_tgt or tgt_in_src:
        return True

    for idx in range(len(tkns_src)):
        starts = " ".join(tkns_src[idx:])
        if starts and target.startswith(starts):
            return True

        ends = " ".join(tkns_src[:-idx])
        if ends and target.endswith(ends):
            return True

    return False


def tokenize(text):
    """Simple tokenizer."""
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = text.split()
    return tokens


def is_json(text: str) -> bool:
    """Check if the text is a valid JSON."""
    try:
        json.loads(text)
        return True
    except json.decoder.JSONDecodeError:
        return False
