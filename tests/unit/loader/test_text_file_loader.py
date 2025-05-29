from exparso.loader.text_file_loader import TextFileLoader
from tests.constants import MARKDOWN_TEXT_DOCUMENT


def test_text_file_loader():
    loader = TextFileLoader()
    pages = loader.load(MARKDOWN_TEXT_DOCUMENT)
    assert len(pages) == 1
    assert pages[0].page_number == 0
    assert pages[0].image is None
    assert pages[0].tables == []
