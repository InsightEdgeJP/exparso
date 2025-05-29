from logging import getLogger

from langchain.output_parsers import PydanticOutputParser
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel

from eval.models import EvalDataModel, Parser, QueryModel, Repository

logger = getLogger(__name__)


class Evaluator:
    def __init__(self, parser: Parser, repository: Repository, query: QueryModel):
        self.parser = parser
        self.repository = repository
        self.query = query
        self.parser_id = f"{self.parser.model_name}-{self.query.display_file_id}"

    def eval(self, llm: BaseChatModel) -> EvalDataModel:
        if result := self.repository.get(self.parser_id):
            if self.query.query_id in result.evals:
                return result.evals[self.query.query_id]
        else:
            result = self.parser.parse(self.query.file)
            self.repository.set(self.parser_id, result)

        page_number = self.query.page_number if len(result.document) > self.query.page_number else 0
        try:
            answer, score = evaluation(self.query.query, self.query.expected, result.document[page_number], llm)
        except Exception as e:
            answer = f"Error {e}"
            score = 0

        eval_data = EvalDataModel(
            query=self.query.query,
            expected=self.query.expected,
            answer=answer,
            rank=score,
            file_id=self.query.display_file_id,
            model=self.parser.model_name,
        )

        result.evals[self.query.query_id] = eval_data
        self.repository.set(self.parser_id, result)
        return eval_data


def evaluation(query: str, expected: str, context: str, client: BaseChatModel) -> tuple[str, int]:

    class RagResult(BaseModel):
        answer: str

    context = context.replace("{", "{{").replace("}", "}}")
    system_message = """You are a helpful assistant.
Please respond to the query using the provided Context.
If the query contains information not included in the Context, reply with "I don’t know".

## Context\n{context}\n
## Query\n{query}\n
## Output\n{instruction}"""
    output_parser = PydanticOutputParser(pydantic_object=RagResult)
    rag_result = (client | output_parser).invoke(
        system_message.format(context=context, instruction=output_parser.get_format_instructions(), query=query)
    )

    class EvalResult(BaseModel):
        rank: int

    system_message = """You are an excellent evaluator.
Please grade the user’s responses to the following questions on a scale of 0 to 100 points.
Provide only the score.

## Example
- If the user’s response is perfect, assign 100 points.
- If the user’s response is incorrect, assign 0 points.
## Query\n{query}\n
## Expected\n{expected}\n
## User Response\n{answer}\n
## Output\n{instruction}
"""
    output_parser = PydanticOutputParser(pydantic_object=EvalResult)
    response = (client | output_parser).invoke(
        system_message.format(
            query=query,
            expected=expected,
            instruction=output_parser.get_format_instructions(),
            answer=rag_result.answer,
        )
    )
    return rag_result.answer, response.rank
