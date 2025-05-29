import pytest

from exparso import parse_document
from tests.constants import PDF_TABLE_DOCUMENT


def test_not_exist_file():
    with pytest.raises(FileNotFoundError):
        parse_document("not_exist_file.txt")


def test_not_support_model():
    with pytest.raises(ValueError):
        parse_document(PDF_TABLE_DOCUMENT, "not_support_model")  # type: ignore


def test_not_support_extension():
    with pytest.raises(ValueError):
        parse_document(__file__)
