from exparso.loader.docx_loader import DocxLoader
from tests.constants import DOCX_DOCUMENT


def test_docx_loader():
    loader = DocxLoader()
    pages = loader.load(DOCX_DOCUMENT)
    assert len(pages) == 1
