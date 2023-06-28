"""Models to be used in the research."""

import openai


def gpt3(prompt: str, max_tokens: int = 1000) -> str:
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


def chatgpt(prompt: str, max_tokens: int = 1000) -> str:
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


def gpt4(prompt: str, max_tokens: int = 1000) -> str:
    """Generate text with GPT-4."""

    message = {"role": "system", "content": f"{prompt}"}

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[message],
        temperature=0,
        max_tokens=max_tokens,
    )

    content = response.to_dict()
    answer = content["choices"][0]["message"]["content"]

    return answer
