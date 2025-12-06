import copy
import json
import logging
from typing import Any

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable, RunnableLambda
from pydantic import BaseModel, Field, ValidationError

from ...model import (
    Cost,
    HumanMessage,
    LlmModel,
    LlmResponse,
    LoadPageContents,
    SystemMessage,
)
from ..prompt import CorePrompt
from ..type import DocumentType, DocumentTypeEnum

logger = logging.getLogger(__name__)


def parse_response(response: LlmResponse) -> DocumentType:
    answer = _try_parse_answer(response.content)
    if answer:
        return DocumentType(types=answer.types, cost=response.cost)

    fallback_types = _fallback_document_types(response.content)
    logger.warning(
        "Failed to parse document type response; falling back to %s. content=%s",
        fallback_types,
        response.content,
    )
    return DocumentType(types=fallback_types, cost=response.cost)


def judge_document_type(
    llm: LlmModel, prompt: CorePrompt
) -> Runnable[LoadPageContents, DocumentType]:
    """ページの内容を分析し、ドキュメントの種類を判定します。言語の判定も行う。"""

    def create_messages(page: LoadPageContents) -> list[SystemMessage | HumanMessage]:
        parser = JsonOutputParser(pydantic_object=_Answer)
        return [
            SystemMessage(
                content=prompt.judge_document_type.format(
                    format_instructions=parser.get_format_instructions(),
                    types_explanation=DocumentTypeEnum.enum_explain(),
                )
            ),
            HumanMessage(
                content="Please analyze this image.",
                image=copy.copy(page.image),
                image_low=True,
            ),
        ]

    model = RunnableLambda(create_messages) | llm | RunnableLambda(parse_response)
    return model


def no_judge() -> Runnable[LoadPageContents, DocumentType]:
    def default_type(page: LoadPageContents) -> DocumentType:
        return DocumentType(types=[], cost=Cost.zero_cost())

    return RunnableLambda(default_type)


class _Answer(BaseModel):
    types: list[DocumentTypeEnum] = Field(
        ..., description="Types of content present in the document."
    )


def _try_parse_answer(content: Any) -> _Answer | None:
    try:
        return _Answer.model_validate(content)
    except ValidationError:
        nested = _extract_nested_payload(content)
        if nested is None:
            return None
        try:
            return _Answer.model_validate(nested)
        except ValidationError:
            return None


def _extract_nested_payload(content: Any) -> dict | None:
    if isinstance(content, dict):
        nested = content.get("output") or content.get("data")
        parsed = _maybe_parse_json(nested)
        return parsed

    if isinstance(content, str):
        return _maybe_parse_json(content)

    return None


def _maybe_parse_json(value: Any) -> dict | None:
    if isinstance(value, dict):
        return value

    if not isinstance(value, str):
        return None

    stripped = value.strip()
    if stripped.startswith("```"):
        stripped = _strip_code_fence(stripped)

    if not stripped.startswith("{"):
        return None

    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        return None

    return parsed if isinstance(parsed, dict) else None


def _strip_code_fence(value: str) -> str:
    stripped = value.strip()
    if stripped.startswith("```"):
        stripped = stripped.lstrip("`")
        newline_index = stripped.find("\n")
        if newline_index != -1:
            stripped = stripped[newline_index + 1 :]
    if stripped.endswith("```"):
        stripped = stripped[:-3]
    return stripped.strip()


def _fallback_document_types(content: Any) -> list[DocumentTypeEnum]:
    # Fall back to a safe default so downstream parsing can continue.
    return [DocumentTypeEnum.IMAGE, DocumentTypeEnum.TEXT]
