from exparso.loader.image_loader import ImageLoader
from tests.constants import BMP_DOCUMENT, JPEG_DOCUMENT


def test_image_loader_jpg():
    loader = ImageLoader()
    pages = loader.load(JPEG_DOCUMENT)
    assert len(pages) == 1
    assert pages[0].page_number == 0
    assert pages[0].image is not None
    assert pages[0].tables == []


def test_image_loader_bmp():
    loader = ImageLoader()
    pages = loader.load(BMP_DOCUMENT)
    assert len(pages) == 1
    assert pages[0].page_number == 0
    assert pages[0].image is not None
    assert pages[0].tables == []
