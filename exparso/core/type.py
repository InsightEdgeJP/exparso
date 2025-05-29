from enum import Enum

from pydantic import BaseModel

from ..model import Cost, LoadPageContents, PageContents


class DocumentTypeEnum(Enum):
    TABLE = "table"
    FLOWCHART = "flowchart"
    GRAPH = "graph"
    IMAGE = "image"
    TEXT = "text"
    TEXT_ONLY = "text_only"

    @staticmethod
    def enum_explain():
        return """
- **table**: Select if the image contains a table, such as a grid or matrix displaying structured data.
- **flowchart**: Select if the image contains a flowchart or diagram illustrating a process or sequence of steps.
- **graph**: Select if the image contains a graph, chart, or plot.
- **image**: Select if the image contains any other image except for tables and graphs.
- **text**: Select if the image contains any text, even if other elements are also present.
- **text_only**: Select if the image contains only text and no other elements.
"""


class DocumentType(BaseModel):
    types: list[DocumentTypeEnum]
    cost: Cost


class ContextData(BaseModel):
    path: str
    cost: Cost
    content: str = ""
    user_context: str | None = None

    def text(self):
        retval = "## path\n" + self.path
        if self.user_context:
            retval += "\n## user_context\n" + self.user_context
        if self.content:
            retval += "\n## content\n" + self.content
        return retval


class ParseDocument(BaseModel):
    new_page: PageContents
    context: ContextData


class InputParseDocument:
    def __init__(
        self,
        page: LoadPageContents,
        context: ContextData,
        document_type: list[DocumentTypeEnum],
    ):
        self.page = page
        self.context = context
        self.document_type = document_type
