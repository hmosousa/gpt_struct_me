# ChatGPT Struct Me

This repository hosts the code used for the development of the **"GPT Struct Me: Probing GPT Models on Narrative Entity Extraction"** paper. The goal of this work was to evaluate the capabilities of generative large language models on the extraction of narrative entities from text. To accomplish that, we used GPT3 and ChatGPT models from OpenAI and evaluate them on the extraction of narrative entities, namely, participants, events, and temporal expressions (timexs). The results obtained indicate that GPT models are competitive with out-of-the-box baseline systems.

## Setup

To use this repository, you need to have access to the [OpenAI models API](https://platform.openai.com/docs/introduction) and provide your API key in a `.env` file. Use the following template for the `.env` file:

```sh
OPENAI_API_KEY="<your_api_key>"
```

## Development Environment

Follow these steps to set up the development environment:

```sh
# Create and activate a virtual environment
virtualenv venv --python=python3.9
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
pip install -e .
```

## Data

The repository utilizes the [Text2Story Lusa Corpus](https://rdm.inesctec.pt/dataset/cs-2023-018) for experiments. To replicate the experiments, download the corpus and place it in a `resources` folder. The directory structure should resemble the following:

```sh
resources
└── lusa_news
    ├── lusa_0.ann
    ├── lusa_0.txt
    ├── lusa_100.ann
    ├── lusa_100.txt
    ├── lusa_101.ann
    └── ...
```

## Models

- **GPT**: For the GPT models we use OpenAI python package and API.
- **Falcon**: The Falcon models have to be cloned to the `resources/models` directory:
  - git clone https://huggingface.co/tiiuae/falcon-7b-instruct
  - git clone https://huggingface.co/tiiuae/falcon-7b
  - git clone https://huggingface.co/tiiuae/falcon-180b

### Launch inference endpoint

To deply locally the models under evalaution we used HuggingFace's [`text_generation_inference`](https://github.com/huggingface/text-generation-inference). After installing all the deppencies needs to run the following command:

```shell
sudo docker run \
  --gpus all \
  --shm-size 1g \
  -p 8080:80 \
  -v $PWD/resources/models/:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id /data/falcon-40b \
  --trust-remote-code 
```

## Results

The following table compares the results obtained from out-of-the-box baselines with the GPT models:

|                   |             |  $P$  |  $R$  | $F_{1}$ | $F_{1_{r}}$ |
|-------------------|-------------|-------|-------|---------|-------------|
| **Timexs**        | TEI2GO      | 50.7  | 59.4  |   54.7  |     55.7    |
|                   | HeidelTime  | 50.1  | 59.3  |   54.2  |     56.3    |
|                   | SRL         | 23.6  | 35.7  |   28.4  |     50.5    |
|                   | GPT-3       | 58.5  | 73.5  |   65.1  |     73.0    |
|                   | ChatGPT     | 34.5  | 58.6  |   43.5  |     48.0    |
| **Participants**  | SRL         | 27.1  | 20.7  |   23.4  |     47.7    |
|                   | GPT-3       | 35.9  | 35.8  |   35.8  |     51.0    |
|                   | ChatGPT     | 40.1  | 46.6  |   43.1  |     47.4    |
| **Events**        | SRL         | 67.1  | 40.4  |   50.4  |     83.5    |
|                   | TEFE        | 95.4  | 9.1   |   16.6  |     95.6    |
|                   | GPT-3       | 41.9  | 53.3  |   46.9  |     51.7    |
|                   | ChatGPT     | 50.7  | 44.3  |   47.2  |     61.4    |

The results show that the combination of the best prompts and GPT models outperform (using strict $F_1$) the baseline in the extraction of participants and time expressions but failed to reach the same results in the extraction of events.

## Run Experiments

All the scripts to replicate the experimentation process are placed on the `experiments` folder. This folder contains three scripts of great importance: 

- `prompt_selection.py` which is used to assess the best prompt template for a given model. If one whiches to select the best prompt template for the `gp4` model, one can do it by executing the following command:  `python experiments/prompt_selection.pt --mid gpt4`.

- After having the produced text by the model one has to parse the answers. This can be made by running the `parse.py` script with the following command `python experiments/parse.py --mode prompt_selection`. This will produce a `predictions.json` on the `results/prompt_selection` folder.

- Having the predictions we are now in a position to compare them with the annotations. By running `python experiments/evalaute.py --mode prompt_selection` one will produce a `results.json` on the `results/prompt_selection` folder that contains the predictions, recall, $F_1$ score, and relaxed $F_1$ score.

- From the values attained by the `evaluate.py` script one can assert what is the best template according to a given criterion. For our research, we consider the strict $F_1$ score. After identifying the best template one has to go to the `constants.py` on the `experiments` folder and add the best template for the model-entity pair. 

- With that done we can now run the `experiments/test.py` script.
  
These scripts are meant to be executed recursively and in the presented order. That is, first, the best template is selected by executing the `prompt_selection.py` script, and only after that, you should run the `test.py` script.

To assert what is the list of models supported, the user can set the `--help` flag on any of the scripts.

## Running Experiments

The `experiments` folder contains scripts to replicate the experimentation process:

1. **Prompt Selection**: To assess the best prompt template for a specific model (e.g., `gpt4`), execute the following command:
   ```sh
   python experiments/prompt_selection.py -m gpt4
   ```

2. **Parsing**: After obtaining the model-generated text, parse the answers using the `parse.py` script:
   ```sh
   python experiments/parse.py --mode prompt_selection
   ```

3. **Evaluation**: To compare predictions with annotations, run the `evaluate.py` script:
   ```sh
   python experiments/evaluate.py --mode prompt_selection
   ```

4. **Template Selection**: Based on evaluation results, identify the best template and add it to the `constants.py` file in the `experiments` folder.

5. **Final Experiment**: Run the `test.py` script to execute the final experiment.
   ```sh
   python experiments/test.py -m gpt4
   ```
   
These scripts should be executed sequentially in the order presented. You can use the `--help` flag on any script to view supported options and commands.
