# 📑 Exparso

本ライブラリは、画像を含むドキュメントのパースを行うためのライブラリです。
テキストとして出力することで、従来のベクトル検索や全文検索での利用を可能することを目的とします。

> [!NOTE]
> 現在、公開に向けて準備中です。

## 💡 使用方法

`parse_document` 関数を利用して、ドキュメントをパースします。

```python
from exparso import parse_document
from langchain_openai import AzureChatOpenAI

llm_model = AzureChatOpenAI(model="gpt-4o")
text = parse_document(path="path/to/document.pdf", model=llm_model)
```

## 📑 対応ファイル

| コンテンツタイプ | 拡張子 |
|-----------------|--------|
| **📑 ドキュメント**  | PDF, PowerPoint |
| **🖼️ 画像**        | JPEG, PNG, BMP |
| **📝 テキストデータ** | テキストファイル, Markdown |
| **📊 表データ**     | Excel, CSV |

## 🔥 LLM

|クラウドベンダー|モデル|
|-|-|
|Azure|GPT|
|Google Cloud|Claude, Gemini|
