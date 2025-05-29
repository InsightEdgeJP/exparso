from ..model import LoadPageContents, PageLoader
from .pdf_loader import PdfLoaderService


class DocxLoader(PageLoader):
    def load(self, path: str) -> list[LoadPageContents]:
        pdf_pages = PdfLoaderService.load(path)
        return pdf_pages
