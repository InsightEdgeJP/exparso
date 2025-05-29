from exparso.loader.pptx_loader import PptxLoader
from tests.constants import PPTX_DOCUMENT


def test_pptx_loader():
    loader = PptxLoader()
    pages = loader.load(PPTX_DOCUMENT)
    assert len(pages) == 3
