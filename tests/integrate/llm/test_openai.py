from langchain_openai import AzureChatOpenAI

from exparso.llm.openai import generate_openai_llm
from exparso.model import HumanMessage, Image, SystemMessage


def test_aoai(azure_chat_openai: AzureChatOpenAI):
    aoai = generate_openai_llm(azure_chat_openai)
    response = aoai.invoke(
        [
            SystemMessage(content="京都は日本の首都ですか" + '# Output\n以下のJson形式に従って下さい\n{"answer":str}'),
        ]
    )
    assert response
    assert response.cost.input_token > 0
    assert response.cost.output_token > 0
    assert "gpt-4o" in response.cost.llm_model_name
    assert "answer" in response.content


def test_aoai_with_image(example_image: Image, azure_chat_openai: AzureChatOpenAI):
    aoai = generate_openai_llm(azure_chat_openai)
    response = aoai.invoke(
        [
            SystemMessage(content="あなたは博識です" + '# Output\n以下のJson形式に従って下さい\n{"answer":str}'),
            HumanMessage(content="これは何色ですか", image=example_image, image_low=True),
        ],
    )
    assert response
    assert response.cost.input_token > 0
    assert response.cost.output_token > 0
    assert "gpt-4o" in response.cost.llm_model_name
    assert "answer" in response.content
