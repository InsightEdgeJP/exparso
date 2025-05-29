from typing import Sequence

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage as _HumanMessage
from langchain_core.messages import SystemMessage as _SystemMessage
from langchain_core.runnables import RunnableLambda

from ..model import Cost, HumanMessage, LlmModel, LlmResponse, SystemMessage


def convert_message(
    messages: Sequence[HumanMessage | SystemMessage],
) -> Sequence[_HumanMessage | _SystemMessage]:
    retval: list[_HumanMessage | _SystemMessage] = []
    for m in messages:
        if isinstance(m, HumanMessage):
            if m.image:
                image_type, base64 = m.image_base64
                retval.append(
                    _HumanMessage(
                        role="user",
                        content=[
                            {"type": "text", "text": m.content},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{image_type};base64,{base64}",
                                },
                                "detail": "low" if m.image_low else "high",
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
    model_name = response.response_metadata.get("model_name", "unknown")
    token_usage = response.response_metadata.get("token_usage", {})
    output_token = token_usage.get("completion_tokens", 0)
    input_token = token_usage.get("prompt_tokens", 0)
    assert isinstance(content, str)
    assert isinstance(model_name, str)
    return LlmResponse(
        content=content,
        cost=Cost(
            input_token=input_token,
            output_token=output_token,
            llm_model_name=model_name,
        ),
    )


def generate_openai_llm(model: BaseChatModel) -> LlmModel:
    return (
        RunnableLambda(convert_message)
        | model.bind(response_format={"type": "json_object"})
        | RunnableLambda(parse_response)
    )
