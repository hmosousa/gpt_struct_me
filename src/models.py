"""Models to be used in the research."""

import json
import os
import logging
import requests
from pathlib import Path

import replicate
import boto3
import dotenv
import openai
import transformers
from transformers import AutoTokenizer
import torch
from text_generation import Client

from src.utils import is_json

logger = logging.getLogger(__name__)


ROOT = Path(__file__).parent.parent
MODELS_PATH = ROOT / "resources" / "models"

dotenv.load_dotenv(ROOT / ".env")

HF_KEY = os.getenv("HF_KEY")
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_KEY")


class Falcon:
    def __init__(self, size: str = "7b", instruct: bool = False):
        """Initialize the Falcon model.
        Args:
            size (str): Size of the model to use. Valid values: "7b", "40b", and "180b". 
        """
        torch.cuda.empty_cache()

        model_name = f"falcon-{size}"
        if instruct:
            model_name += "-instruct"
        model_path = MODELS_PATH / model_name

        logger.info(f"Loading Falcon model from {model_path}.")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=model_path,
            tokenizer=self.tokenizer,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            device_map="auto",
        )

    def __call__(self, prompt: str) -> str:
        logger.info(f"Generating answer for prompt:\n{prompt}")
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        input_n_tokens = input_ids.shape[1]
        output = self.pipeline(
            prompt,
            max_length=2 * input_n_tokens,
            do_sample=False,  # Ensure deterministic results.
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,  # For open-ended generation.
            pad_token_id=self.tokenizer.eos_token_id,
            use_cache=False,
        )
        answer = output[0]["generated_text"]
        answer = answer.strip(prompt)
        return answer


class Llama2InferenceAPI:
    def __init__(self, size: str = "70b", chat: bool = False):
        """Initialize the Llama model.
        Args:
            size (str): Size of the model to use. Valid values: "70b" and "370b". 
        """
        if chat:
            model_name = f"Llama-2-{size}-chat-hf"
        else:
            model_name = f"Llama-2-{size}-hf"

        self.endpoint = f"https://api-inference.huggingface.co/models/meta-llama/{model_name}"
        self.headers = {"Authorization": f"Bearer {HF_KEY}"}
        
    def __call__(self, prompt: str) -> str:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1_000,
                "do_sample": False,
                "return_full_text": False,
            },
            "options": {
                "wait_for_model": True,
                "use_cache": False,
            }
        }

        response = requests.post(self.endpoint, headers=self.headers, json=payload)
        output = response.json()
        answer = output[0]["generated_text"]
        return answer


def gpt3(prompt: str, max_tokens: int = 800) -> str:
    """Generate text with GPT-3."""
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=max_tokens,
    )

    content = response.to_dict()
    answer = content["choices"][0]["text"]

    return answer


def chatgpt(prompt: str, max_tokens: int = 800) -> str:
    """Generate text with ChatGPT."""

    message = {"role": "system", "content": f"{prompt}"}

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message],
        temperature=0,
        max_tokens=max_tokens,
    )

    content = response.to_dict()
    answer = content["choices"][0]["message"]["content"]

    return answer


def gpt4(prompt: str, max_tokens: int = 800) -> str:
    """Generate text with GPT-4."""

    message = {"role": "system", "content": f"{prompt}"}

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[message],
        temperature=0.0,
        max_tokens=max_tokens,
    )

    content = response.to_dict()
    answer = content["choices"][0]["message"]["content"]

    return answer


class SagemakerEndpoint:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.runtime = boto3.Session().client('sagemaker-runtime')

    def __call__(self, prompt: str) -> str:
        payload = json.dumps({
            "inputs": "My name is Julien and I like to",
            "parameters": {
                "eos_token_id": 2,
                "pad_token_id": 2,
                "max_length": 4096,
                "temperature": 0,
                "do_sample": False,
                "num_return_sequences": 1,
            },
        })

        response = self.runtime.invoke_endpoint(
            EndpointName=self.endpoint,
            ContentType="application/json",
            Body=payload
        )
        answer = response["Body"].read().decode("utf-8")
        return answer


class HFInferenceLocal:
    """A model deployed locally in 
    [Text Generation Inference](https://github.com/huggingface/text-generation-inference) 
    container from  Hugging Face."""

    def __init__(self, url: str = "http://127.0.0.1:8080"):
        self.client = Client(url, timeout=300)

    def __call__(self, prompt: str, max_tokens: int = 1_000) -> str:
        reponse = self.client.generate(
            prompt=prompt,
            max_new_tokens=max_tokens,
            do_sample=False
        )
        answer = reponse.generated_text
        return answer


def llama2_70b(prompt: str, max_tokens: int = 800) -> str:
    """API from [Replicate](https://replicate.com/). To minimize the number of tokens generated, 
    this function checks if the tokens generated are valid JSON. If not, it continues generating 
    until the max_tokens in reached."""
    
    payload = {
        "prompt": prompt,
        "max_new_tokens": max_tokens,
        "temperature": 0.01,
        "seed": 123,
        "top_k": 1
    }
    
    generator = replicate.run(
        "meta/llama-2-70b:a52e56fee2269a78c9279800ec88898cecb6c8f1df22a6483132bea266648f00",
        input=payload
    )

    tokens = []
    for item in generator:
        tokens.append(item)
        answer = "".join(tokens)
        if is_json(answer):
            return answer
    return answer
