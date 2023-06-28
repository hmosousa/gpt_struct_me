"""Evaluation functions."""

from typing import Dict, Tuple, Set

from src.utils import string_overlap, tokenize


def recall_score(tp: int, fn: int) -> float:
    """Compute the recall score."""
    return tp / (tp + fn) if tp + fn > 0 else 0


def precision_score(tp: int, fp: int) -> float:
    """Compute the precision score."""
    return tp / (tp + fp) if tp + fp > 0 else 0


def f1_score(tp: int, fp: int, fn: int) -> float:
    """Compute the F1 score."""
    p = precision_score(tp, fp)
    r = recall_score(tp, fn)
    return 2 * (p * r) / (p + r) if p + r > 0 else 0


def strict_metrics(prediction: list, annotation: list) -> dict:
    """Compute micro-averaged metrics for a given entity."""

    tps, fns, fps = 0, 0, 0
    for doc_id in prediction:

        pred = set(prediction[doc_id])
        annt = set(annotation[doc_id])

        tp, fp, fn = exact_match(pred, annt)

        tps += tp
        fps += fp
        fns += fn

    recall = recall_score(tps, fns)
    precision = precision_score(tps, fps)
    f1 = f1_score(tps, fps, fns)

    return {"recall": recall, "precision": precision, "f1": f1}


def exact_match(prediction: set, annotation: set) -> tuple:
    """Compute the TP, FP, FN for a set of predictions and annotations."""
    tp = len(prediction.intersection(annotation))
    fp = len(prediction.difference(annotation))
    fn = len(annotation.difference(prediction))
    return tp, fp, fn


def relaxed_metrics(prediction: Dict, annotation: Dict) -> dict:
    """Compute micro-averaged metrics for a given entity."""
    f1 = 0
    for doc_id in prediction:
        pred = set(prediction[doc_id])
        annt = set(annotation[doc_id])
        f1 += macro_averaged_f1_score(pred, annt)
    f1 /= len(prediction)
    return {"f1": f1}


def macro_averaged_f1_score(pred: Set[str], annt: Set[str]) -> float:
    """Compute the macro-averaged F1 score for a set of predictions and annotations."""
    f1 = 0
    for pred_entity in pred:

        # Tokens that are in the prediction.
        tkns_pred = set(tokenize(pred_entity))

        # Annotated tokens that overlap with the prediction.
        match_entites = [
            annt_entity
            for annt_entity in annt
            if string_overlap(pred_entity, annt_entity)
        ]
        tkns_match = set(tokenize(" ".join(match_entites)))

        tp, fp, fn = exact_match(tkns_pred, tkns_match)
        f1 += f1_score(tp, fp, fn)

    macro_avg_f1 = f1 / len(pred) if len(pred) > 0 else 0
    return macro_avg_f1
