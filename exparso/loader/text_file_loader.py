from ..model import LoadPageContents, PageLoader


class TextFileLoader(PageLoader):
    def load(self, path: str) -> list[LoadPageContents]:
        with open(path, "r") as f:
            contents = f.read()
        return [
            LoadPageContents(
                contents=contents,
                page_number=0,
                image=None,
                tables=[],
            )
        ]
