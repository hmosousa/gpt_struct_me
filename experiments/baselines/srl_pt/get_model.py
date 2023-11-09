# The model is split between this repository and Huggingface
# This script unites the two parts and creates a folder for the 
# complete allennlp srl model.

import sys
import os
from shutil import copyfile

# from transformers import AutoModel, AutoTokenizer
import torch
from allennlp.data.vocabulary import Vocabulary

from my_model import SrlMyModel


if __name__ == "__main__":
    model_name = sys.argv[1]

    vocab = Vocabulary()
    vocab = vocab.from_files("Models/" + model_name + "/Vocabulary") 
    ll = torch.load("Models/" + model_name + "/linear_layer.pt")

    model = SrlMyModel(vocab = vocab, bert_model = "liaad/" + model_name)
    model.tag_projection_layer.load_state_dict(ll)

    if not os.path.exists(model_name):
        os.mkdir(model_name)

    torch.save(model.state_dict(), model_name + "/weights.th")
    model.vocab.save_to_files(model_name + "/vocabulary")
    copyfile("Models/" + model_name + "/config.json", model_name + "/config.json")
