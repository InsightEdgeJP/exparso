from exparso.core.docs_type.judge_document_type import parse_response
from exparso.core.type import DocumentTypeEnum
from exparso.model import Cost, LlmResponse


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
