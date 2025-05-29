from exparso.loader.pdf_loader import PdfLoader
from tests.constants import PDF_TABLE_DOCUMENT


def test_pdf_loader_with_tables():
    loader = PdfLoader()
    pages = loader.load(PDF_TABLE_DOCUMENT)
    assert len(pages) == 2
    assert pages[0].page_number == 0
    assert pages[0].image
    assert pages[0].tables

    assert pages[1].page_number == 1
    assert pages[1].image
    assert pages[1].tables
