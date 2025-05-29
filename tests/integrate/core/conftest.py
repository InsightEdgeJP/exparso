import pytest


@pytest.fixture
def llm_model(chat_vertex_ai):
    from exparso.llm.gemini import generate_gemini_llm

    return generate_gemini_llm(chat_vertex_ai)
