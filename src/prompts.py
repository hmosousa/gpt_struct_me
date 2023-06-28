"""Build prompts for query the models."""

import json
from string import Template

from src.base import Document
from src.meta import ENTITIES


class Prompter:
    """Prompt generator."""

    def __init__(
        self,
        task: str,
        entity: str,
        example: Document = None,
        definition: bool = False,
    ):
        self.task = task
        self.entity = entity

        template = []
        if task == "extraction":
            template.append(f"Task:\n"
                            f"Extract all {self.entity}.")

            output_format = "JSON-parseable list of strings."
            self.annotation_extraction = self._get_extraction_annotation

        elif task == "classification":
            template.append(f"Task:\n"
                            f"Extract and classify all {self.entity}\n\n"
                            f"Classes:\n"
                            f"{ENTITIES[self.entity]['classes']}")

            output_format = "JSON-parseable list where each element is a list with two strings. " \
                            "The first string is the entity and the second is the class."
            self.annotation_extraction = self._get_classification_annotation

        else:
            raise ValueError(f"Task {task} not supported.")

        if definition:
            template.append(f"Definition:\n"
                            f"{ENTITIES[self.entity]['definition']}")

        if example is not None:
            example_annt = self.annotation_extraction(example)
            example_annt_str = json.dumps(example_annt)
            template.append(f"Example:\n"
                            f"\tInput:\n"
                            f"\t\"{example.text}\"\n"
                            f"\tOutput:\n"
                            f"\t{example_annt_str}")

        template.append(f"Format:\n"
                        f"{output_format}")

        template = "\n\n".join(template)
        self.template = Template(
            f"{template}\n\nInput:\n\"$text\"\n\nOutput:\n")

    def _get_extraction_annotation(self, doc):
        """Get the annotation for the extraction task."""
        if self.entity == "event triggers":
            return [ent.text for ent in doc.events]
        elif self.entity == "time expressions":
            return [ent.text for ent in doc.timexs]
        elif self.entity == "participants":
            return [ent.text for ent in doc.participants]
        else:
            raise ValueError(f"Entity {self.entity} not supported.")

    def _get_classification_annotation(self, doc):
        """Get the annotation for the classification task."""
        if self.entity == "event triggers":
            return [
                (ent.text, ent.class_) if hasattr(ent, "class_")
                else (ent.text, None)
                for ent in doc.events
            ]
        elif self.entity == "time expressions":
            return [
                (ent.text, ent.time_type) if hasattr(ent, "time_type")
                else (ent.text, None)
                for ent in doc.timexs
            ]
        elif self.entity == "participants":
            return [
                (ent.text, ent.participant_type_domain) if hasattr(ent, "participant_type_domain")
                else (ent.text, None)
                for ent in doc.participants
            ]
        else:
            raise ValueError(f"Entity {self.entity} not supported.")

    def generate(self, text: Document) -> str:
        """Generate a zero shot prompt."""
        prompt = self.template.substitute(text=text)
        return prompt
