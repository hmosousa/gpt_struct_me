from src.models import gpt4, llama2_70b, Falcon, Llama2InferenceAPI, SagemakerEndpoint, HFInferenceLocal

PROMPT = """Task:
Extract and classify all participants

Classes:
Person, Organization, Object, Location, Nature, Facility, and Other

Definition:
Participants refer to individuals, groups, organizations, or other entities that are actively involved in or impacted by an event or state. They are typically identified based on their relevance and significance to the situation, and may be explicitly mentioned or inferred from the context. Participants can take on a variety of roles, such as actors, agents, patients, victims, or observers, and their actions and interactions can shape the course of events.

Format:
JSON-parseable list where each element is a list with two strings. The first string is the entity and the second is the class.

Input:
"Violência doméstica: Pulseira eletrónica para homem detido em Penafiel
Um homem de 39 anos foi colocado sob vigilância eletrónica, em Penafiel, distrito do Porto, suspeito de violência física, injúrias e ameaças de morte à ex-companheira, de 42 anos, informou hoje fonte da GNR.
Em comunicado, a autoridade policial indicou que o suspeito "não aceitou a separação e começou a perseguir a vítima na sua residência e no local de trabalho".
A mulher já usava um botão de pânico, que lhe tinha sido aplicado por medida de proteção por teleassistência.
O homem, com antecedentes criminais por ilícitos da mesma natureza, ficou ainda proibido de contactar a vítima."

Output:
"""


def test_gpt4():
    answer = gpt4(PROMPT)
    assert isinstance(answer, str)


def test_falcon7b():
    model = Falcon("40b")
    answer = model(PROMPT)
    assert isinstance(answer, str)


def test_llama_2_7b_chat():
    model = Llama2InferenceAPI("7b", chat=True)
    answer = model(PROMPT)
    assert isinstance(answer, str)


def test_llama_2_13b_chat():
    model = Llama2InferenceAPI("13b", chat=True)
    answer = model(PROMPT)
    assert isinstance(answer, str)


def test_llama_2_70b_chat():
    model = Llama2InferenceAPI("70b", chat=True)
    answer = model(PROMPT)
    assert isinstance(answer, str)


def test_llama_2_7b():
    model = Llama2InferenceAPI("7b", chat=False)
    answer = model(PROMPT)
    assert isinstance(answer, str)


def test_llama_2_13b():
    model = Llama2InferenceAPI("13b", chat=False)
    answer = model(PROMPT)
    assert isinstance(answer, str)


def test_llama_2_70b():
    answer = llama2_70b(PROMPT, max_tokens=20)
    assert isinstance(answer, str)


def test_sagemaker():
    model = SagemakerEndpoint()
    answer = model(PROMPT)
    assert isinstance(answer, str)


def test_hf_local():
    model = HFInferenceLocal()
    answer = model(PROMPT, max_tokens=20)
    assert isinstance(answer, str)


def test_hf_local2():
    model = HFInferenceLocal()
    answer = model("Give me a list of the top 10 dive sites you would recommend around the world.", max_tokens=30)
    assert isinstance(answer, str)


if __name__ == "__main__":
    test_gpt4()
