from typing import Sequence

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage as _HumanMessage
from langchain_core.runnables import RunnableLambda

from ..model import Cost, HumanMessage, LlmModel, LlmResponse, SystemMessage


def convert_message(
    messages: Sequence[HumanMessage | SystemMessage],
) -> Sequence[_HumanMessage | str]:
    MAX_IMAGE_LENGTH = 384.0  # low resolution解析のための画像サイズ

    retval: list[str | _HumanMessage] = []
    for m in messages:
        if isinstance(m, HumanMessage):
            if m.image:
                if m.image_low:
                    large_length = max(m.image.width, m.image.height)
                    scale = MAX_IMAGE_LENGTH / large_length
                    m.scale_image(scale)
                mime_type, base64 = m.image_base64
                retval.append(
                    _HumanMessage(
                        role="user",
                        content=[
                            m.content,
                            {"type": "media", "mime_type": mime_type, "data": base64},
                        ],
                    )
                )

            else:
                retval.append(m.content)
        elif isinstance(m, SystemMessage):
            retval.append(m.content)
    return retval


def generate_gemini_llm(model: BaseChatModel) -> LlmModel:
    def parse_response(response: AIMessage) -> LlmResponse:
        content = response.content
        input_token = response.usage_metadata.get("input_tokens", 0) if response.usage_metadata else 0
        output_token = response.usage_metadata.get("output_tokens", 0) if response.usage_metadata else 0
        assert isinstance(content, str)
        return LlmResponse(
            content=content,
            cost=Cost(
                input_token=input_token,
                output_token=output_token,
                llm_model_name=model.model_name if model.model_name else "unknown",  # type: ignore
            ),
        )

    return RunnableLambda(convert_message) | model | RunnableLambda(parse_response)
