import logging
import json
import os
import sys
import re
from typing import Iterator, List, Optional

from allennlp.commands.predict import _PredictManager
from allennlp.common.file_utils import cached_path
from allennlp.common.util import JsonDict
from allennlp.data import DatasetReader, Instance
from allennlp.models import Model
from allennlp.models.archival import load_archive
from allennlp.predictors.predictor import Predictor
from allennlp_models.structured_prediction.predictors import \
    SemanticRoleLabelerPredictor
from nltk import download, tokenize
from overrides import overrides

import conll_reader
import my_model
import my_reader

download('punkt')


logging.getLogger('allennlp').setLevel(logging.WARNING)


@Predictor.register("my_predictor")
class predict(SemanticRoleLabelerPredictor):
    def __init__(
        self, model: Model, dataset_reader: DatasetReader
    ) -> None:
        super().__init__(model, dataset_reader, "pt_core_news_sm")

    @overrides
    def load_line(self, line: str) -> Iterator[str]:
        for sentence in tokenize.sent_tokenize(line):
            yield sentence

    @overrides
    def dump_line(self, outputs) -> str:
        
        output_file = "output.txt"
        if os.path.exists(output_file):
            with open("output.txt", "r", encoding="utf-8") as f:
                content = json.load(f)
        else:
            content = []

        result = content + [outputs]
        with open("output.txt", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False)

    @overrides
    def _sentence_to_srl_instances(self, sentence):
        new_sent = ""
        for char in sentence:
            new_sent += char if char != "-" else " -"
        tokens = self._tokenizer.tokenize(new_sent)
        return self.tokens_to_instances(tokens)

    @overrides
    def predict_json(self, inputs: str):
        instances = self._sentence_to_srl_instances(inputs)
        if not instances:
            return inputs.split()
        return self.predict_instances(instances)

    @overrides
    def predict_instances(self, instances: List[Instance]) -> JsonDict:
        outputs = self._model.forward_on_instances(instances)
        results = {
            "verbs": [], 
            "words": outputs[0]["words"]
        }
        for output in outputs:
            tags = output["tags"]
            description = self.make_srl_string(output["words"], tags)
            verbs = {
                "verb": output["verb"], 
                "description": description, 
                "tags": tags
            } 
            results["verbs"].append(verbs)
        return results


class predictManager(_PredictManager):
    def __init__(
            self,
            predictor: Predictor,
            input_file: str,
            output_file: Optional[str],
            batch_size: int,
            print_to_console: bool,
            has_dataset_reader: bool):
        super().__init__(predictor, input_file, output_file, batch_size, print_to_console, has_dataset_reader)

    @overrides
    def _get_json_data(self) -> Iterator[str]:
        if self._input_file == "-":
            for line in sys.stdin:
                if not line.isspace():
                    yield from self._predictor.load_line(line)
        else:
            input_file = cached_path(self._input_file)
            with open(input_file, "r", encoding="utf-8") as file_input:
                for line in file_input:
                    if not line.isspace():
                        yield from self._predictor.load_line(line)

