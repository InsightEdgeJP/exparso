import vertexai
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_vertexai import ChatVertexAI

from eval.settings import settings


def create_llm() -> BaseChatModel:
    vertexai.init(project=settings.gcp_project, location="us-central1")
    llm = ChatVertexAI(model_name="gemini-1.5-pro-002")
    return llm
