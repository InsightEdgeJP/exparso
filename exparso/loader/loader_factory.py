from ..model import PageLoader
from .csv_loader import CsvLoader
from .docx_loader import DocxLoader
from .image_loader import ImageLoader
from .pdf_loader import PdfLoader
from .pptx_loader import PptxLoader
from .text_file_loader import TextFileLoader
from .xlsx_loader import XlsxLoader


class LoaderFactory:
    @staticmethod
    def create(extension: str) -> PageLoader:
        extension = extension.lower()
        if extension == "pdf":
            return PdfLoader()
        elif extension in ["txt", "md"]:
            return TextFileLoader()
        elif extension == "csv":
            return CsvLoader()
        elif extension in ["xlsx", "xls"]:
            return XlsxLoader()
        elif extension in ["jpg", "jpeg", "png", "bmp", "gif"]:
            return ImageLoader()
        elif extension in ["docx", "doc"]:
            return DocxLoader()
        elif extension == "pptx":
            return PptxLoader()
        else:
            raise ValueError("Unsupported file extension")
