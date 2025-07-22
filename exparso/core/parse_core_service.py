import logging
from typing import Optional

from langchain_core.runnables import RunnableConfig
from tenacity import retry, stop_after_attempt, wait_fixed

from ..model import Cost, Document, LlmModel, LoadPageContents, PageContents
from .context import update_context
from .docs_type import judge_document_type, no_judge
from .parse import parse_document
from .prompt import CorePrompt
from .type import ContextData, DocumentType, DocumentTypeEnum, InputParseDocument, ParseDocument

logger = logging.getLogger(__name__)


class ParseCoreService:
    def __init__(
        self,
        llm: LlmModel,
        file_path: str,
        prompt: CorePrompt,
        user_context: Optional[str],
        config: Optional[RunnableConfig] = None,
    ) -> None:
        self.parser = parse_document(llm, prompt=prompt)
        self.context_updater = update_context(llm, prompt=prompt)
        self.judge_document = judge_document_type(llm, prompt=prompt)
        self.context = ContextData(path=file_path, cost=Cost.zero_cost(), user_context=user_context)
        self.config = config

    def __call__(
        self,
        contents: list[LoadPageContents],
    ) -> Document:
        parsed_contents: list[PageContents] = []

        for i, page in enumerate(contents):
            logger.debug(f"Start Parse Page {page.page_number}")

            document_type = self.__judge_document_type(page)
            self.context.cost += document_type.cost

            # 画像認識が必要ない場合は余計な処理を行わない
            if DocumentTypeEnum.TEXT_ONLY in document_type.types or not document_type.types:
                logger.debug("Document Type is Text Only")
                # テキストのみの場合でも基本的な内容は保持する
                parsed_contents.append(PageContents.from_load_data(page))
                continue

            input_parse_document = InputParseDocument(
                page=page,
                context=self.context,
                document_type=document_type.types,
            )
            parsed_document = self.__parse_document(input_parse_document)
            parsed_contents.append(parsed_document.new_page)

            if i != len(contents) - 1:
                self.context = self.__update_context(parsed_document)
            logger.debug(f"End Parse Page {page.page_number}")

        return Document(contents=parsed_contents, cost=self.context.cost)

    @retry(
        # retry=retry_if_exception_type(ValidationError),
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
    )
    def __judge_document_type(self, page: LoadPageContents) -> DocumentType:
        judge_document = self.judge_document if page.image else no_judge()
        return judge_document.invoke(page, config=self.config)

    @retry(
        # retry=retry_if_exception_type(ValidationError),
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
    )
    def __parse_document(self, input_parse_document: InputParseDocument) -> ParseDocument:
        return self.parser.invoke(input_parse_document, config=self.config)

    @retry(
        # retry=retry_if_exception_type(ValidationError),
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
    )
    def __update_context(self, parsed_document: ParseDocument) -> ContextData:
        return self.context_updater.invoke(parsed_document, config=self.config)
