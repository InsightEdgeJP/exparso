from langchain_google_vertexai.model_garden import ChatAnthropicVertex

from exparso.llm.claude import generate_claude_llm
from exparso.model import HumanMessage, Image, SystemMessage


def test_chat_anthropic_vertex(chat_anthropic_vertex: ChatAnthropicVertex):

    model = generate_claude_llm(chat_anthropic_vertex)
    response = model.invoke(
        [
            SystemMessage(
                content='# Output\n以下のJson形式に従って下さい\n"answer":str',
            ),
            HumanMessage(content="京都は日本の首都ですか?"),
        ]
    )
    assert response
    assert response.cost.input_token > 0
    assert response.cost.output_token > 0
    assert response.content
    assert "answer" in response.content


def test_chat_anthropic_vertex_with_image(example_image: Image, chat_anthropic_vertex: ChatAnthropicVertex):
    model = generate_claude_llm(chat_anthropic_vertex)
    response = model.invoke(
        [
            SystemMessage(
                content="あなたは博識です" + '# Output\n以下のJson形式に従って下さい\n"answer":str',
            ),
            HumanMessage(content="これは何色ですか", image=example_image, image_low=True),
        ]
    )
    assert response
    assert response.cost.input_token > 0
    assert response.cost.output_token > 0
    assert response.content
    assert "answer" in response.content
