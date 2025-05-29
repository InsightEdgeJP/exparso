from exparso.model import Cost, Document, PageContents


def test_document():
    document = Document(
        contents=[
            PageContents(
                contents="",
                page_number=0,
            )
        ],
        cost=Cost(input_token=0, output_token=0, llm_model_name="aoai"),
    )
    assert document.contents
