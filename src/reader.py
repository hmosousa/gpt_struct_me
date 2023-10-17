"""Dataset readers."""

from pathlib import Path
from typing import List

import tieval
from tieval import datasets

from src.base import LusaDocument, TimebankDocument, Document
from src.parser import AnnParser


def read_lusa(dirpath: Path) -> List[Document]:
    """Read Lusa news dataset."""
    ann_parser = AnnParser()

    documents = []
    for filepath in dirpath.glob("*.txt"):

        text = filepath.read_text().strip()

        annpath = filepath.with_suffix(".ann")
        ann = annpath.read_text()
        annotation = ann_parser.parse(ann)

        document = LusaDocument(filepath.stem, text, annotation)
        documents.append(document)
    return documents


def read_timebank(dirpath: Path) -> List[Document]:
    """Read TimeBank corpus."""
    timebank = datasets.read("timebank", dirpath.parent)

    documents = []
    for doc in timebank.documents:

        text = doc.text

        annotation = [entity.__dict__ for entity in doc.entities]

        document = TimebankDocument(doc.name, text, annotation)
        documents.append(document)
    return documents
    