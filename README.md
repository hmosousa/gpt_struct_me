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
└── lusa
    ├── lusa_0.ann
    ├── lusa_0.txt
    ├── lusa_100.ann
    ├── lusa_100.txt
    ├── lusa_101.ann
    └── ...
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
