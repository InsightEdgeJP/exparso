from exparso.loader.xlsx_loader import XlsxLoader
from tests.constants import XLSX_DOCUMENT


def test_csv_loader():
    loader = XlsxLoader()
    pages = loader.load(XLSX_DOCUMENT)
    assert len(pages) == 2
    assert pages[0].page_number == 0
    assert pages[0].image is None
    assert pages[0].tables == [
        [["Name", "Age", "Occpation"], ["John", 33, "Engineer"], ["Bob", 29, "Designer"], ["Alice", 49, "Manager"]]
    ]
    assert pages[0].contents.startswith("Sheet1\n")
