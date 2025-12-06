import csv
from typing import Sequence

from ..model import LoadPageContents, PageLoader


class CsvLoader(PageLoader):
    def load(self, path: str) -> list[LoadPageContents]:
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            table = [row for row in reader]

        markdown = self._to_markdown(table)

        page_contents = LoadPageContents(
            contents=markdown,
            page_number=0,
            image=None,
            tables=[table],
        )
        return [page_contents]

    @staticmethod
    def _to_markdown(table: Sequence[Sequence[str]]) -> str:
        if not table:
            return ""

        def format_row(row: Sequence[str]) -> str:
            cells = [cell if cell is not None else "" for cell in row]
            return "| " + " | ".join(cells) + " |"

        header = table[0]
        body = table[1:]
        lines = [format_row(header)]
        separator = "| " + " | ".join(["---"] * len(header or [""])) + " |"
        lines.append(separator)
        for row in body:
            lines.append(format_row(row))

        return "\n".join(lines)
