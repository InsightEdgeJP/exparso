import logging

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel, RunnablePassthrough
from pydantic import BaseModel

from ...model import HumanMessage, LlmModel, LlmResponse, PageContents, SystemMessage
from ..prompt import CorePrompt
from ..type import DocumentTypeEnum, InputParseDocument, ParseDocument

logger = logging.getLogger(__name__)


def parse_document(llm: LlmModel, prompt: CorePrompt) -> Runnable[InputParseDocument, ParseDocument]:
    def integrate(*args, **kwargs) -> ParseDocument:
        response = args[0]["response"]
        input_parse_document = args[0]["passthrough"]
        assert isinstance(response, LlmResponse) and isinstance(input_parse_document, InputParseDocument)
        answer = _Answer.model_validate(response.content)
        input_parse_document.context.cost += response.cost
        return ParseDocument(
            new_page=PageContents(contents=answer.output, page_number=input_parse_document.page.page_number),
            context=input_parse_document.context,
        )

    def create_messages(input_parse_document: InputParseDocument) -> list[SystemMessage | HumanMessage]:
        system_prompt = generate_system_message(input_parse_document.document_type, input_parse_document.context.text())
        human_prompt = HumanMessage(
            content=prompt.extract_human_message(input_parse_document.page.contents),
            image=input_parse_document.page.image,
        )

        messages: list[SystemMessage | HumanMessage] = [system_prompt, human_prompt]
        return messages

    def generate_system_message(types: list[DocumentTypeEnum], context: str) -> SystemMessage:
        parser = JsonOutputParser(pydantic_object=_Answer)
        retval = ""
        if DocumentTypeEnum.IMAGE in types:
            retval += prompt.image_prompt
        if DocumentTypeEnum.FLOWCHART in types:
            retval += prompt.flowchart_prompt
        if DocumentTypeEnum.TABLE in types:
            retval += prompt.table_prompt
        if DocumentTypeEnum.GRAPH in types:
            retval += prompt.graph_prompt

        system_prompt = prompt.extract_document.format(
            document_type_prompt=retval, context=context, format_instruction=parser.get_format_instructions()
        )
        return SystemMessage(content=system_prompt)

    model = RunnableParallel(
        response=RunnableLambda(create_messages) | llm, passthrough=RunnablePassthrough()
    ) | RunnableLambda(integrate)
    return model


class _Answer(BaseModel):
    output: str
