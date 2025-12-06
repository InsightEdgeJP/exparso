import json
import logging
from typing import Any, Sequence

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage as _HumanMessage
from langchain_core.messages import SystemMessage as _SystemMessage
from langchain_core.runnables import RunnableLambda

from ..model import Cost, HumanMessage, LlmModel, LlmResponse, SystemMessage

logger = logging.getLogger(__name__)


def convert_message(
    messages: Sequence[HumanMessage | SystemMessage],
) -> Sequence[_HumanMessage | _SystemMessage]:
    retval: list[_HumanMessage | _SystemMessage] = []
    for message in messages:
        if isinstance(message, HumanMessage):
            parts: list[dict[str, Any]] = []
            if message.content:
                parts.append({"type": "text", "text": message.content})
            if message.image:
                mime, base64_data = message.image_base64
                if mime and base64_data:
                    parts.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{base64_data}"},
                        }
                    )

            if not parts:
                payload: Any = ""
            elif len(parts) == 1 and parts[0]["type"] == "text":
                payload = parts[0]["text"]
            else:
                payload = parts

            retval.append(_HumanMessage(role="user", content=payload))
        elif isinstance(message, SystemMessage):
            retval.append(_SystemMessage(role="system", content=message.content))
    return retval


def _safe_int(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _ensure_json_content(content: str) -> str:
    stripped = content.strip()
    stripped = _strip_markdown_code_block(stripped)
    if stripped.startswith("{") and stripped.endswith("}"):
        parsed = _try_load_dict(stripped)
        if parsed is not None:
            return json.dumps(parsed, ensure_ascii=False)
        return stripped

    fallback = {"output": stripped}
    return json.dumps(fallback, ensure_ascii=False)


def _strip_markdown_code_block(text: str) -> str:
    if not text.startswith("```"):
        return text

    lines = text.splitlines()
    if not lines:
        return text

    # drop opening fence
    lines = lines[1:]
    # drop closing fence if present
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]

    return "\n".join(lines).strip()


def _try_load_dict(text: str) -> dict[str, Any] | None:
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        return None

    if isinstance(loaded, dict):
        return loaded
    return None


def parse_response(response: BaseMessage) -> LlmResponse:
    logger.debug("Ollama normalized response: %s", response)
    content = response.content
    if isinstance(content, list):
        text_parts: list[str] = []
        for part in content:
            if isinstance(part, str):
                text_parts.append(part)
            elif isinstance(part, dict):
                text = part.get("text")
                if isinstance(text, str):
                    text_parts.append(text)
        content = "".join(text_parts)
    if not isinstance(content, str):
        content = str(content)
    content = _ensure_json_content(content)
    logger.debug("Ollama normalized response: %s", content)

    metadata = getattr(response, "response_metadata", {}) or {}
    usage = getattr(response, "usage_metadata", {}) or {}
    input_token = _safe_int(
        usage.get("input_tokens", metadata.get("prompt_eval_count"))
    )
    output_token = _safe_int(usage.get("output_tokens", metadata.get("eval_count")))
    model_name = metadata.get("model", "ollama")

    return LlmResponse(
        content=content,
        cost=Cost(
            input_token=input_token,
            output_token=output_token,
            llm_model_name=model_name,
        ),
    )


def generate_ollama_llm(model: BaseChatModel) -> LlmModel:
    return RunnableLambda(convert_message) | model | RunnableLambda(parse_response)
