import pytest
from PIL import Image

from exparso.core.parse.parse_document import parse_document
from exparso.core.prompt import JAPANESE_CORE_PROMPT
from exparso.core.type import ContextData, DocumentTypeEnum, InputParseDocument
from exparso.model import Cost, LlmModel, LoadPageContents


@pytest.fixture
def page() -> LoadPageContents:
    img = Image.new("RGB", (100, 100), color="red")
    return LoadPageContents(contents="contents", image=img, page_number=1, tables=[])


def test_parse_document(llm_model: LlmModel, page: LoadPageContents):
    input = InputParseDocument(
        page=page,
        context=ContextData(path="path", cost=Cost.zero_cost(), content="content"),
        document_type=[DocumentTypeEnum.IMAGE],
    )
    model = parse_document(llm_model, JAPANESE_CORE_PROMPT)
    assert model.invoke(input)
