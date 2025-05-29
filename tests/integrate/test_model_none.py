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


def test_model_none_with_pdf():
    documents = parse_document(PDF_TABLE_DOCUMENT)
    assert documents


def test_model_none_with_text():
    documents = parse_document(MARKDOWN_TEXT_DOCUMENT)
    assert documents


def test_model_none_with_jpg():
    documents = parse_document(JPEG_DOCUMENT)
    assert documents


def test_model_none_with_bmp():
    documents = parse_document(BMP_DOCUMENT)
    assert documents


def test_model_none_with_csv():
    documents = parse_document(CSV_DOCUMENT)
    assert documents


def test_model_none_with_xlsx():
    documents = parse_document(XLSX_DOCUMENT)
    assert documents


def test_model_none_with_pptx():
    documents = parse_document(PPTX_DOCUMENT)
    assert documents


def test_model_none_with_docx():
    documents = parse_document(DOCX_DOCUMENT)
    assert documents
