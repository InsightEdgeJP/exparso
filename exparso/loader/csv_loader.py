import csv

from ..model import LoadPageContents, PageLoader


class CsvLoader(PageLoader):
    def load(self, path: str) -> list[LoadPageContents]:
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            # Convert CSV rows into a list of lists (table)
            table = [row for row in reader]

            # Create a PageContents object with the table and other fields set as required
            page_contents = LoadPageContents(
                contents=file.read(),
                page_number=0,
                image=None,
                tables=[table],
            )
        return [page_contents]
