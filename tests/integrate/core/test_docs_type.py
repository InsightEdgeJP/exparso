import pytest
from PIL import Image

from exparso.core.docs_type import judge_document_type
from exparso.core.prompt import JAPANESE_CORE_PROMPT
from exparso.model import LlmModel, LoadPageContents


@pytest.fixture
def page() -> LoadPageContents:
    img = Image.new("RGB", (100, 100), color="red")
    return LoadPageContents(contents="contents", image=img, page_number=1, tables=[])


def test_docs_type(llm_model: LlmModel, page: LoadPageContents):
    test_docs_type = judge_document_type(llm_model, JAPANESE_CORE_PROMPT)
    assert test_docs_type.invoke(page)
