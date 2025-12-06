import json

import pytest

from exparso.core.parse.parse_document import _parse_llm_answer


def test_parse_llm_answer_accepts_string_output():
    content = {"output": "extracted text"}

    answer = _parse_llm_answer(content)

    assert answer.output == "extracted text"


def test_parse_llm_answer_coerces_dict_output():
    payload = {"output": {"title": "", "description": ""}}

    answer = _parse_llm_answer(payload)

    assert answer.output == json.dumps(payload["output"], ensure_ascii=False)


def test_parse_llm_answer_raises_without_output():
    with pytest.raises(Exception):
        _parse_llm_answer({"result": "missing"})
