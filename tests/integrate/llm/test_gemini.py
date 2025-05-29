from langchain_google_vertexai import ChatVertexAI

from exparso.llm.gemini import generate_gemini_llm
from exparso.model import HumanMessage, Image, SystemMessage


def test_gemini_vertexai(chat_vertex_ai: ChatVertexAI):
    gemini = generate_gemini_llm(chat_vertex_ai)
    response = gemini.invoke(
        [
            SystemMessage(
                content="京都は日本の首都ですか" + '\n# Output\n以下のJson形式に従って下さい\n{"answer":str}'
            ),
        ]
    )
    assert response
    assert response.cost.input_token > 0
    assert response.cost.output_token > 0
    assert response.cost.llm_model_name
    assert "answer" in response.content


def test_gemini_vertexai_with_image(example_image: Image, chat_vertex_ai: ChatVertexAI):
    gemini = generate_gemini_llm(chat_vertex_ai)
    response = gemini.invoke(
        [
            SystemMessage(content='あなたは博識です\n # Output\n以下のJson形式に従って下さい\n"answer":str'),
            HumanMessage(content="これは何色ですか", image=example_image, image_low=True),
        ]
    )
    assert response
    assert response.cost.input_token > 0
    assert response.cost.output_token > 0
    assert "answer" in response.content
