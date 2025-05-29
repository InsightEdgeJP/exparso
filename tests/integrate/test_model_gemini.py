import pytest
from langchain_google_vertexai import ChatVertexAI

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


def test_model_gemini_with_pdf(chat_vertex_ai: ChatVertexAI):
    documents = parse_document(PDF_TABLE_DOCUMENT, chat_vertex_ai)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_gemini_with_text(chat_vertex_ai: ChatVertexAI):
    documents = parse_document(MARKDOWN_TEXT_DOCUMENT, chat_vertex_ai)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_gemini_with_jpg(chat_vertex_ai: ChatVertexAI):
    documents = parse_document(JPEG_DOCUMENT, chat_vertex_ai)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_gemini_with_bmp(chat_vertex_ai: ChatVertexAI):
    documents = parse_document(BMP_DOCUMENT, chat_vertex_ai)
    assert documents


def test_model_gemini_with_csv(chat_vertex_ai: ChatVertexAI):
    documents = parse_document(CSV_DOCUMENT, chat_vertex_ai)
    assert documents


def test_model_gemini_with_xlsx(chat_vertex_ai: ChatVertexAI):
    documents = parse_document(XLSX_DOCUMENT, chat_vertex_ai)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_gemini_with_pptx(chat_vertex_ai: ChatVertexAI):
    documents = parse_document(PPTX_DOCUMENT, chat_vertex_ai)
    assert documents


@pytest.mark.skip(reason="API料金の節約")
def test_model_gemini_with_docx(chat_vertex_ai: ChatVertexAI):
    documents = parse_document(DOCX_DOCUMENT, chat_vertex_ai)
    assert documents
