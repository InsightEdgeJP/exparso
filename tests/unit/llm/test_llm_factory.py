import os

import vertexai
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai.model_garden import ChatAnthropicVertex
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from exparso.llm.llm_factory import LlmFactory


def test_azure_chat_openai():
    os.environ["AZURE_OPENAI_API_KEY"] = "dummy"
    os.environ["OPENAI_API_VERSION"] = "2023-05-15"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "dummy"
    model = AzureChatOpenAI()
    assert model.__class__.__name__ == "AzureChatOpenAI"
    llm = LlmFactory.create(model)
    assert llm


def test_chat_openai():
    model = ChatOpenAI(api_key="dummy")  # type: ignore
    assert model.__class__.__name__ == "ChatOpenAI"
    llm = LlmFactory.create(model)
    assert llm


def test_chat_anthropic_vertex():
    llm = ChatAnthropicVertex(
        model_name="dummy-model",
        location="dummy-location",
        project="dummy-project",
    )

    model = LlmFactory.create(llm)
    assert model


def test_chat_vertextai():
    vertexai.init(project="dummy-project", location="us-east1")
    llm = ChatVertexAI(model_name="dummy-model")
    model = LlmFactory.create(llm)
    assert model
