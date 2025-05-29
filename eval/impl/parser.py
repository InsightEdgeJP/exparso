import logging

import pymupdf4llm
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentContentFormat
from azure.identity import DefaultAzureCredential
from docling.document_converter import DocumentConverter
from langchain_core.language_models.chat_models import BaseChatModel
from langfuse.callback import CallbackHandler

from eval.models import FileModel, ParseDataModel, Parser
from eval.settings import settings
from exparso import parse_document

logger = logging.getLogger(__name__)


class Exparso(Parser):
    def __init__(self, model: BaseChatModel, model_name: str):
        self.llm_model_name = model_name
        self.model = model

    def parse(self, file: FileModel) -> ParseDataModel:
        if settings.langfuse_host:
            langfuse_handler = CallbackHandler(
                trace_name=file.id,
                user_id=self.llm_model_name,
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host,
            )
            config = {"callbacks": [langfuse_handler]}
        else:
            config = None
        docs = parse_document(file.path, self.model, config=config)  # type: ignore
        retval = ParseDataModel(
            file_id=file.id,
            model=self.llm_model_name,
            document=[d.contents for d in docs.contents],
        )
        return retval

    @property
    def model_name(self) -> str:
        return self.llm_model_name


class Pymupdf4llm(Parser):
    def parse(self, file: FileModel) -> ParseDataModel:
        md_text = pymupdf4llm.to_markdown(file.path)
        retval = ParseDataModel(file_id=file.id, model="pymupdf4llm", document=[md_text])
        return retval

    @property
    def model_name(self) -> str:
        return "pymupdf4llm"


class AzureDocumentIntelligence(Parser):
    def parse(self, file: FileModel) -> ParseDataModel:
        credential = DefaultAzureCredential()
        client = DocumentIntelligenceClient(endpoint=settings.azure_document_endpoint, credential=credential)
        with open(file.path, "rb") as f:
            response = client.begin_analyze_document(
                model_id="prebuilt-layout",
                body=f,
                output_content_format=DocumentContentFormat.MARKDOWN,
                content_type="application/octet-stream",
            )
        result = response.result().content.split("<!-- PageBreak -->")
        retval = ParseDataModel(file_id=file.id, model="azure-document-intelligence", document=result)
        return retval

    @property
    def model_name(self) -> str:
        return "azure-document-intelligence"


class Docling(Parser):
    def parse(self, file: FileModel) -> ParseDataModel:
        converter = DocumentConverter()
        result = converter.convert(file.path)
        md_text = result.document.export_to_markdown()
        retval = ParseDataModel(file_id=file.id, model="docling", document=[md_text])
        return retval

    @property
    def model_name(self) -> str:
        return "docling"
