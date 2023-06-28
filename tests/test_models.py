from src.models import gpt4


def test_gpt4():
    prompt = "Hello, my name is"
    answer = gpt4(prompt)
    assert isinstance(answer, str)


if __name__ == "__main__":
    test_gpt4()
    