import os

import pytest
import vertexai
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai.model_garden import ChatAnthropicVertex
from langchain_openai import AzureChatOpenAI


@pytest.fixture
def chat_vertex_ai() -> ChatVertexAI:
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash-002")
    region = os.getenv("GEMINI_REGION", "us-central1")
    project = os.getenv("GCP_PROJECT", "")
    vertexai.init(project=project, location=region)
    return ChatVertexAI(model_name=model_name)


@pytest.fixture
def azure_chat_openai() -> AzureChatOpenAI:
    return AzureChatOpenAI(model="gpt-4o", api_version="2024-06-01")


@pytest.fixture
def chat_anthropic_vertex() -> ChatAnthropicVertex:
    model = os.getenv("CLAUDE_MODEL_NAME", "claude-3-5-sonnet-v2@20241022")
    region = os.getenv("CLAUDE_REGION", "us-east5")
    project = os.getenv("GCP_PROJECT", "")
    return ChatAnthropicVertex(
        model_name=model,
        location=region,
        project=project,
    )
