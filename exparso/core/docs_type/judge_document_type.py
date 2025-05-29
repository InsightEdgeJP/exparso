import copy
import logging

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable, RunnableLambda
from pydantic import BaseModel, Field

from ...model import Cost, HumanMessage, LlmModel, LlmResponse, LoadPageContents, SystemMessage
from ..prompt import CorePrompt
from ..type import DocumentType, DocumentTypeEnum

logger = logging.getLogger(__name__)


def parse_response(response: LlmResponse) -> DocumentType:
    answer = _Answer.model_validate(response.content)
    return DocumentType(types=answer.types, cost=response.cost)


def judge_document_type(llm: LlmModel, prompt: CorePrompt) -> Runnable[LoadPageContents, DocumentType]:
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
            HumanMessage(content="Please analyze this image.", image=copy.copy(page.image), image_low=True),
        ]

    model = RunnableLambda(create_messages) | llm | RunnableLambda(parse_response)
    return model


def no_judge() -> Runnable[LoadPageContents, DocumentType]:
    def default_type(page: LoadPageContents) -> DocumentType:
        return DocumentType(types=[], cost=Cost.zero_cost())

    return RunnableLambda(default_type)


class _Answer(BaseModel):
    types: list[DocumentTypeEnum] = Field(..., description="Types of content present in the document.")
