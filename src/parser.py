"""Parser Lusa news dataset annotations."""

import re
from collections import defaultdict

from src.base import Document


class AnnParser:
    """Parse Lusa news dataset annotations."""

    entity_regex = re.compile(
        r"(\w+)\t(Event|Time|Spatial_Relation|Participant|Measure) (.*)\t(.*)")
    annotator_note_regex = re.compile(r"#\d+\tAnnotatorNotes (.*)\t(.*)")

    def parse(self, annotation: str) -> Document:
        """Parse a file with the BRAT annotation."""

        annotation = annotation.strip()

        tags = []
        attributes = defaultdict(list)
        lines = annotation.split("\n")
        for line in lines:
            if line[0] == "T":
                tags.append(self._parse_entity(line))

            elif line[0] == "R":
                tags.append(self._parse_link(line))

            elif line[0] == "A":
                attrib = self._parse_attribute(line)
                id_ = attrib.pop("id")
                attributes[id_].append(attrib)

            elif line[0] == "#":
                attribs = self._parse_annotator_notes(line)
                for attrib in attribs:
                    id_ = attrib.pop("id")
                    attributes[id_].append(attrib)

        # Add attributes to tags.
        for tag in tags:
            for attrib in attributes[tag["id"]]:
                key = attrib["attrib"].lower()
                value = attrib["value"]
                tag[key] = value

        return tags

    def _parse_entity(self, line: str) -> dict:
        tid, type_, offset, text = self.entity_regex.findall(line)[0]
        return {"id": tid, "type": type_, "offset": offset, "text": text}

    @staticmethod
    def _parse_link(line: str) -> dict:
        rid, relation, src, tgt = line.split()
        type_, value = relation.split("_")
        src = src.split(":")[1]
        tgt = tgt.split(":")[1]
        return {"id": rid, "type": type_, "relation": value, "src": src, "tgt": tgt}

    @staticmethod
    def _parse_attribute(line: str) -> dict:
        aid, attrib, id_, value = line.split()
        return {"aid": aid, "attrib": attrib, "value": value, "id": id_}

    def _parse_annotator_notes(self, line: str) -> list:
        attributes = []
        id_, attribs = self.annotator_note_regex.findall(line)[0]
        for attrib in attribs.split():
            type_, value = attrib.split("=")
            attributes.append({"attrib": type_, "value": value, "id": id_})
        return attributes
