import pytest
from langchain_google_vertexai.model_garden import ChatAnthropicVertex

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


def test_model_claude_with_pdf(chat_anthropic_vertex: ChatAnthropicVertex):
    documents = parse_document(PDF_TABLE_DOCUMENT, chat_anthropic_vertex)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_claude_with_text(chat_anthropic_vertex: ChatAnthropicVertex):
    documents = parse_document(MARKDOWN_TEXT_DOCUMENT, chat_anthropic_vertex)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_claude_with_jpg(chat_anthropic_vertex: ChatAnthropicVertex):
    documents = parse_document(JPEG_DOCUMENT, chat_anthropic_vertex)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_claude_with_bmp(chat_anthropic_vertex: ChatAnthropicVertex):
    documents = parse_document(BMP_DOCUMENT, chat_anthropic_vertex)
    assert documents


def test_model_claude_with_csv(chat_anthropic_vertex: ChatAnthropicVertex):
    documents = parse_document(CSV_DOCUMENT, chat_anthropic_vertex)
    assert documents


def test_model_claude_with_xlsx(chat_anthropic_vertex: ChatAnthropicVertex):
    documents = parse_document(XLSX_DOCUMENT, chat_anthropic_vertex)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_claude_with_pptx(chat_anthropic_vertex: ChatAnthropicVertex):
    documents = parse_document(PPTX_DOCUMENT, chat_anthropic_vertex)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_claude_with_docx(chat_anthropic_vertex: ChatAnthropicVertex):
    documents = parse_document(DOCX_DOCUMENT, chat_anthropic_vertex)
    assert documents
