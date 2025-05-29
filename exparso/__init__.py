import logging
import os
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import RunnableConfig

from .core import JAPANESE_CORE_PROMPT, CorePrompt, ParseCoreService
from .llm import LlmFactory
from .loader import LoaderFactory
from .model import Document

logger = logging.getLogger(__name__)


def parse_document(
    path: str,
    model: Optional[BaseChatModel] = None,
    context: Optional[str] = None,
    prompt: CorePrompt = JAPANESE_CORE_PROMPT,
    config: Optional[RunnableConfig] = None,
) -> Document:
    """ドキュメントをMLLMによって読み込む

    Args:
        path (str): ファイルパス
        model (BaseChatModel): langchain's BaseChatModel
        context (str): ユーザーコンテキスト
        config (dict, optional): LLM Input 設定. Defaults to None.
    Returns:
        Document: ドキュメントの情報
    """

    # ファイルが存在しない場合はエラーを出力
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    # 拡張子から適したLoaderを呼び出す
    extension = os.path.basename(path).split(".")[-1]
    loader = LoaderFactory.create(extension)
    logger.debug(f"Loader is {loader.__class__.__name__}")

    # モデル名からインスタンスを生成する
    llm_model = LlmFactory.create(model)
    llm_model_name = llm_model.__class__.__name__ if llm_model else "None"
    logger.debug(f"MLLM model is {llm_model_name}")

    # ファイルを読み込む
    raw_contents = loader.load(path)
    logger.debug(f"Loaded {len(raw_contents)} pages")
    logger.debug("Start Parse Document")

    if not llm_model:
        logger.warning("MLLM model is not defined.")
        return Document.from_load_data(raw_contents)

    # LLMによる処理を行う
    parser = ParseCoreService(llm=llm_model, file_path=path, prompt=prompt, user_context=context, config=config)
    doc = parser(contents=raw_contents)
    return doc
