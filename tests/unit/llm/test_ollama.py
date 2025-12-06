from PIL import Image
from langchain_core.messages import HumanMessage as LangchainHumanMessage

from exparso.llm.ollama import convert_message
from exparso.model import HumanMessage, SystemMessage


def test_convert_message_text_only_keeps_string():
    message = HumanMessage(content="hello")

    converted = convert_message([message])

    assert isinstance(converted[0], LangchainHumanMessage)
    assert converted[0].content == "hello"


def test_convert_message_includes_base64_image_payload():
    image = Image.new("RGB", (2, 2), color="white")
    message = HumanMessage(content="describe", image=image)

    converted = convert_message([SystemMessage(content="sys"), message])

    human_message = converted[1]
    assert isinstance(human_message, LangchainHumanMessage)
    assert isinstance(human_message.content, list)
    assert human_message.content[0] == {"type": "text", "text": "describe"}
    image_part = human_message.content[1]
    assert image_part["type"] == "image_url"
    assert image_part["image_url"]["url"].startswith("data:image/png;base64,")
