from dataclasses import dataclass
from typing import Sequence

from .image import Image


@dataclass
class LoadPageContents:
    contents: str
    page_number: int
    image: Image | None
    tables: Sequence[Sequence[Sequence[str | None]]]


@dataclass
class PageContents:
    contents: str
    page_number: int

    @classmethod
    def from_load_data(cls, data: LoadPageContents) -> "PageContents":
        return cls(
            contents=data.contents,
            page_number=data.page_number,
        )
