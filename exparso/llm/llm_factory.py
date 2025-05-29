from langchain_core.language_models.chat_models import BaseChatModel

from ..model import LlmModel
from .claude import generate_claude_llm
from .gemini import generate_gemini_llm
from .openai import generate_openai_llm


class LlmFactory:
    @staticmethod
    def create(model: BaseChatModel | None) -> LlmModel | None:
        if not model:
            return None

        model_name = model.__class__.__name__
        if model_name == "AzureChatOpenAI" or model_name == "ChatOpenAI":
            return generate_openai_llm(model)
        elif "ChatAnthropic" in model_name:
            return generate_claude_llm(model)
        elif "ChatVertexAI" in model_name:
            return generate_gemini_llm(model)
        else:
            raise ValueError(f"Unsupported model: {model_name}")
