from exparso.core.docs_type import no_judge
from exparso.core.docs_type.judge_document_type import parse_response
from exparso.core.type import DocumentTypeEnum
from exparso.model import Cost, LoadPageContents, LlmResponse


def _response(payload: str) -> LlmResponse:
    return LlmResponse(content=payload, cost=Cost.zero_cost())


def test_parse_response_handles_nested_output_json():
    payload = '{"output": "{\\"types\\": [\\"image\\"], \\"notes\\": \\"ok\\"}"}'
    response = _response(payload)

    document_type = parse_response(response)

    assert document_type.types == [DocumentTypeEnum.IMAGE]


def test_parse_response_falls_back_when_types_missing():
    payload = '{"output": "Unable to comply"}'
    response = _response(payload)

    document_type = parse_response(response)

    assert document_type.types == [DocumentTypeEnum.IMAGE, DocumentTypeEnum.TEXT]


def test_no_judge_marks_pages_with_tables_as_table_types():
    page = LoadPageContents(
        contents="| Name | Age |",
        page_number=0,
        image=None,
        tables=[[["Name", "Age"]]],
    )

    document_type = no_judge().invoke(page)

    assert document_type.types == [DocumentTypeEnum.TABLE]


def test_no_judge_marks_other_pages_as_text_only():
    page = LoadPageContents(contents="text", page_number=0, image=None, tables=[])

    document_type = no_judge().invoke(page)

    assert document_type.types == [DocumentTypeEnum.TEXT_ONLY]
