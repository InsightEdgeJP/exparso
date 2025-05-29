import logging

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel
from pydantic import BaseModel

from ...model import HumanMessage, LlmModel, LlmResponse, SystemMessage
from ..prompt import CorePrompt
from ..type import ContextData, ParseDocument

logger = logging.getLogger(__name__)


def update_context(llm: LlmModel, prompt: CorePrompt) -> Runnable[ParseDocument, ContextData]:
    def pass_through(data: ParseDocument) -> ContextData:
        return data.context

    def integrate(*args, **kwargs) -> ContextData:
        new = args[0]["new"]
        old = args[0]["old"]
        assert isinstance(new, ContextData) and isinstance(old, ContextData)

        return ContextData(
            path=old.path,
            cost=new.cost + old.cost,
            content=new.content,
            user_context=old.user_context,
        )

    def create_messages(data: ParseDocument) -> list[SystemMessage | HumanMessage]:
        parser = JsonOutputParser(pydantic_object=_Answer)
        system_prompt = SystemMessage(
            content=prompt.update_context.format(
                context=data.context.text(), format_instructions=parser.get_format_instructions()
            ),
        )
        return [system_prompt, HumanMessage(data.new_page.contents)]

    update_model = RunnableLambda(create_messages) | llm | RunnableLambda(parse)
    model = RunnableParallel(new=update_model, old=RunnableLambda(pass_through)) | RunnableLambda(integrate)
    return model


def parse(response: LlmResponse) -> ContextData:
    answer = _Answer.model_validate(response.content)
    return ContextData(
        path="",
        cost=response.cost,
        content=answer.context,
        user_context="",
    )


class _Answer(BaseModel):
    context: str
