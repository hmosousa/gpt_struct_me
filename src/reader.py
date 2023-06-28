"""Dataset readers."""

from pathlib import Path
from typing import List

from src.base import Document
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

        document = Document(filepath.stem, text, annotation)
        documents.append(document)
    return documents
