from exparso.core.context import update_context
from exparso.core.prompt import JAPANESE_CORE_PROMPT
from exparso.core.type import ContextData, ParseDocument
from exparso.model import Cost, LlmModel, PageContents


def test_update_context(llm_model: LlmModel):
    context = ContextData(
        path="名簿.xlsx",
        content="",
        cost=Cost.zero_cost(),
    )
    new_page = PageContents(
        contents="たなか けんじ 男 30歳\nやまだ さちこ 女 25歳\n",
        page_number=1,
    )
    data = ParseDocument(
        new_page=new_page,
        context=context,
    )
    model = update_context(llm_model, prompt=JAPANESE_CORE_PROMPT)
    context = model.invoke(data)
    assert context
    assert context.cost.input_token > 0
    assert context.content
    assert context.path == "名簿.xlsx"
