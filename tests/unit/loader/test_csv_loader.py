from exparso.loader.csv_loader import CsvLoader
from tests.constants import CSV_DOCUMENT


def test_csv_loader():
    loader = CsvLoader()
    pages = loader.load(CSV_DOCUMENT)
    assert len(pages) == 1
    assert pages[0].page_number == 0
    assert pages[0].image is None
    assert pages[0].tables == [
        [
            ["Name", "Age", "Occupation"],
            ["Alice", "30", "Engineer"],
            ["Bob", "25", "Designer"],
            ["Charlie", "35", "Manager"],
        ]
    ]
