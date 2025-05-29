from typing import Sequence

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage as _HumanMessage
from langchain_core.messages import SystemMessage as _SystemMessage
from langchain_core.runnables import RunnableLambda

from ..model import Cost, HumanMessage, LlmModel, LlmResponse, SystemMessage


def convert_message(messages: Sequence[HumanMessage | SystemMessage]) -> Sequence[_HumanMessage | _SystemMessage]:
    retval: list[_HumanMessage | _SystemMessage] = []
    MAX_IMAGE_LENGTH = 384.0
    for m in messages:
        if isinstance(m, HumanMessage):
            if m.image:
                if m.image_low:
                    large_length = max(m.image.width, m.image.height)
                    scale = MAX_IMAGE_LENGTH / large_length
                    m.scale_image(scale)
                media_type, base64 = m.image_base64
                retval.append(
                    _HumanMessage(
                        role="user",
                        content=[
                            {"type": "text", "text": m.content},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": base64,
                                },
                            },
                        ],
                    )
                )
            else:
                retval.append(_HumanMessage(role="user", content=m.content))
        elif isinstance(m, SystemMessage):
            retval.append(_SystemMessage(role="system", content=m.content))
    return retval


def parse_response(response: BaseMessage) -> LlmResponse:
    assert isinstance(response, BaseMessage)
    content = response.content
    cost = Cost(
        input_token=response.response_metadata.get("usage", {}).get("input_tokens", 0),
        output_token=response.response_metadata.get("usage", {}).get("output_tokens", 0),
        llm_model_name=response.response_metadata.get("model", "unknown"),
    )
    assert isinstance(content, str)
    return LlmResponse(content=content, cost=cost)


def generate_claude_llm(model: BaseChatModel) -> LlmModel:
    return RunnableLambda(convert_message) | model | RunnableLambda(parse_response)
