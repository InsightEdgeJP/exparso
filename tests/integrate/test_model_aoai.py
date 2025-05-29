from langchain_openai import AzureChatOpenAI

from exparso import parse_document
from tests.constants import (
    BMP_DOCUMENT,
    CSV_DOCUMENT,
    DOCX_DOCUMENT,
    JPEG_DOCUMENT,
    MARKDOWN_TEXT_DOCUMENT,
    PDF_TABLE_DOCUMENT,
    PPTX_DOCUMENT,
    XLSX_DOCUMENT,
)


def test_model_aoai_with_pdf(azure_chat_openai: AzureChatOpenAI):
    documents = parse_document(PDF_TABLE_DOCUMENT, azure_chat_openai)
    assert documents


def test_model_aoai_with_text(azure_chat_openai: AzureChatOpenAI):
    documents = parse_document(MARKDOWN_TEXT_DOCUMENT, azure_chat_openai)
    assert documents


def test_model_aoai_with_jpg(azure_chat_openai: AzureChatOpenAI):
    documents = parse_document(JPEG_DOCUMENT, azure_chat_openai)
    assert documents


def test_model_aoai_with_bmp(azure_chat_openai: AzureChatOpenAI):
    documents = parse_document(BMP_DOCUMENT, azure_chat_openai)
    assert documents


def test_model_aoai_with_csv(azure_chat_openai: AzureChatOpenAI):
    documents = parse_document(CSV_DOCUMENT, azure_chat_openai)
    assert documents


def test_model_aoai_with_xlsx(azure_chat_openai: AzureChatOpenAI):
    documents = parse_document(XLSX_DOCUMENT, azure_chat_openai)
    assert documents


def test_model_aoai_with_pptx(azure_chat_openai: AzureChatOpenAI):
    documents = parse_document(PPTX_DOCUMENT, azure_chat_openai)
    assert documents


def test_model_aoai_with_docx(azure_chat_openai: AzureChatOpenAI):
    documents = parse_document(DOCX_DOCUMENT, azure_chat_openai)
    assert documents
