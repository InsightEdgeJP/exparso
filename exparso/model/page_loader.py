from abc import abstractmethod

from .page_contents import LoadPageContents


class PageLoader:
    @abstractmethod
    def load(self, path: str) -> list[LoadPageContents]:
        pass
