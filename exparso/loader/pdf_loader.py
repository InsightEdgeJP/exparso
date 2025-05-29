import os
import subprocess
import tempfile

import pdfplumber
from pdfplumber.page import Page

from ..model import LoadPageContents, PageLoader


class PdfLoader(PageLoader):
    def load(self, path: str) -> list[LoadPageContents]:
        pages = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                pages.append(self._load_page(page))
        return pages

    def _load_page(self, page: Page) -> LoadPageContents:
        return LoadPageContents(
            page_number=page.page_number - 1,
            contents=page.extract_text(),
            tables=page.extract_tables(),  # type: ignore
            image=page.to_image().original,
        )


class PdfLoaderService:
    @staticmethod
    def load(path: str) -> list[LoadPageContents]:
        loader = PdfLoader()
        pdf_filename = os.path.splitext(os.path.basename(path))[0] + ".pdf"
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = f"{tmpdir}/{pdf_filename}"
            process = subprocess.run(
                [
                    "soffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    tmpdir,
                    path,
                ]
            )
            if process.returncode != 0:
                return []

            pdf_pages = loader.load(pdf_path)
            loader = PdfLoader()
        return pdf_pages
