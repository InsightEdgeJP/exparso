# 🔧 プロンプトのカスタマイズ

## 📝 `CorePrompt`クラスの概要

`exparso/core/prompt/prompt.py`に定義されている`CorePrompt`クラスは、ドキュメント処理のための様々なプロンプトを管理します。このクラスを使用することで、ライブラリの動作をカスタマイズし、特定のユースケースに合わせたプロンプトを注入することができます。

## 🚀 `CorePrompt`の使用方法

### 基本的な使用例

`CorePrompt`クラスをライブラリのエントリーポイントとして使用するには、以下の手順に従います：

```python
from exparso import parse_document
from exparso.core.prompt.prompt import CorePrompt
from langchain_openai import AzureChatOpenAI

# カスタムプロンプトの定義
custom_prompts = CorePrompt(
    judge_document_type="ドキュメントタイプを判定してください: {types_explanation} {format_instructions}",
    extract_document="内容を抽出してください: {document_type_prompt} {context} {format_instruction}",
    update_context="コンテキストを更新してください: {context} {format_instructions}",
    table_prompt="テーブルデータを抽出してください。",
    flowchart_prompt="フローチャートデータを抽出してください。",
    graph_prompt="グラフデータを抽出してください。",
    image_prompt="画像データを抽出してください。",
    extract_document_text_prompt="テキストを抽出してください: {document_text}",
    extract_image_only_prompt="画像からテキストを抽出してください: {document_text}"
)

# LLMモデルの設定
llm_model = AzureChatOpenAI(model="gpt-4o")

# カスタムプロンプトを使用してドキュメントをパース
text = parse_document(
    path="path/to/document.pdf",
    model=llm_model,
    context="このドキュメントは...",
    prompt=custom_prompts
)
```

## 📋 プロンプトの種類と役割

`CorePrompt`クラスの各フィールドは、ライブラリの特定の機能に対応しています：

| プロンプト名 | 役割 | 必須プレースホルダー |
|------------|------|-------------------|
| `judge_document_type` | ドキュメントタイプの判定 | `{types_explanation}`, `{format_instructions}` |
| `extract_document` | ドキュメント内容の抽出 | `{document_type_prompt}`, `{context}`, `{format_instruction}` |
| `update_context` | コンテキスト情報の更新 | `{context}`, `{format_instructions}` |
| `table_prompt` | テーブルデータの抽出 | なし |
| `flowchart_prompt` | フローチャートデータの抽出 | なし |
| `graph_prompt` | グラフデータの抽出 | なし |
| `image_prompt` | 画像データの抽出 | なし |
| `extract_document_text_prompt` | ドキュメントからのテキスト抽出 | `{document_text}` |
| `extract_image_only_prompt` | 画像からのテキスト抽出 | `{document_text}` |

## 🔍 ユースケース別の例

### 📊 業界特化型プロンプト（医療分野の例）

```python
from exparso import parse_document
from exparso.core.prompt.prompt import CorePrompt
from langchain_openai import AzureChatOpenAI

# 医療分野向けカスタムプロンプト
medical_prompts = CorePrompt(
    judge_document_type="この医療文書のタイプを判定してください: {types_explanation} {format_instructions}",
    extract_document="この医療文書から臨床情報を抽出してください: {document_type_prompt} 患者情報: {context} {format_instruction}",
    update_context="患者の医療記録を更新してください: {context} {format_instructions}",
    table_prompt="この検査結果表から異常値を特定してください。",
    image_prompt="この医療画像から所見を詳細に説明してください。",
    # 他のフィールドはデフォルト値を使用
)

llm_model = AzureChatOpenAI(model="gpt-4o")

# 医療文書の解析
text = parse_document(
    path="path/to/medical_report.pdf",
    model=llm_model,
    context="患者ID: 12345, 年齢: 45歳, 既往歴: 高血圧",
    prompt=medical_prompts
)
```

### 🌐 多言語対応プロンプト

```python
from exparso import parse_document
from exparso.core.prompt.prompt import CorePrompt
from langchain_google_vertexai import ChatVertexAI

# 言語に応じたプロンプトを取得する関数
def get_language_prompt(language="ja"):
    if language == "en":
        return CorePrompt(
            judge_document_type="Please determine the document type: {types_explanation} {format_instructions}",
            extract_document="Please extract content from this document: {document_type_prompt} Context: {context} {format_instruction}",
            # 他のフィールドは省略
        )
    else:  # デフォルトは日本語
        return CorePrompt(
            judge_document_type="ドキュメントタイプを判定してください: {types_explanation} {format_instructions}",
            extract_document="内容を抽出してください: {document_type_prompt} コンテキスト: {context} {format_instruction}",
            # 他のフィールドは省略
        )

# 英語ドキュメント用のプロンプトを取得
english_prompt = get_language_prompt("en")

# LLMモデルの設定
llm_model = ChatVertexAI(model_name="gemini-1.5-pro-002")

# 英語ドキュメントの解析
text = parse_document(
    path="path/to/english_document.pdf",
    model=llm_model,
    context="This document is about...",
    prompt=english_prompt
)
```

## ⚠️ 注意事項

1. すべての必須プレースホルダーが含まれていることを確認してください
2. 複雑なプロンプトは事前にテストして期待通りの結果が得られることを確認してください