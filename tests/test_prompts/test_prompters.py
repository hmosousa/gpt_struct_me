from src.prompts import OneShotPrompter


class TestOneShotPrompter:

    def test_generate(self):
        text = "This is a test input."
        annotation = ["This", "test"]
        prompter = OneShotPrompter(text, annotation)
        prompt = prompter.generate("Second input")

        expected_prompt = "Input: This is a test input.\nOutput: [\"This\", \"test\"]\nInput: Second input\nOutput: "
        assert prompt == expected_prompt
