from .cost import Cost
from .page_contents import LoadPageContents, PageContents


class Document:
    contents: list[PageContents]
    cost: Cost

    def __init__(self, contents: list[PageContents], cost: Cost):
        self.contents = contents
        self.cost = cost

    @classmethod
    def from_load_data(cls, load_data: list[LoadPageContents]) -> "Document":
        return cls(
            contents=[PageContents.from_load_data(data) for data in load_data],
            cost=Cost.zero_cost(),
        )
