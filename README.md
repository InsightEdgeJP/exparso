# 📑 Exparso

![python](https://img.shields.io/badge/python-%20%203.10%20|%203.11%20|%203.12-blue)

本ライブラリは、画像を含むドキュメントのパースを行うためのライブラリです。
テキストとして出力することで、従来のベクトル検索や全文検索での利用を可能することを目的とします。
[](<より詳しい情報に関しては、[こちら](https://congenial-waddle-5krzvq6.pages.github.io/)を参照してください。>)

## 📥 インストール方法

### LibreOffice

Office ファイルをテキストに変換するために、LibreOffice をインストールします。

```bash
# Ubuntu
sudo apt install libreoffice

# Mac
brew install --cask libreoffice
```

### ライブラリのインストール

```bash
pip install exparso
```

## 💡 使用方法

`parse_document` 関数を利用して、ドキュメントをパースします。

```python
from exparso import parse_document
from langchain_openai import AzureChatOpenAI

llm_model = AzureChatOpenAI(model="gpt-4o")
text = parse_document(path="path/to/document.pdf", model=llm_model)
```

## 📑 対応ファイル

| コンテンツタイプ      | 拡張子                     |
| --------------------- | -------------------------- |
| **📑 ドキュメント**   | PDF, PowerPoint            |
| **🖼️ 画像**           | JPEG, PNG, BMP             |
| **📝 テキストデータ** | テキストファイル, Markdown |
| **📊 表データ**       | Excel, CSV                 |

## 🔥 LLM

| クラウドベンダー | モデル                                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| Azure            | ChatGPT(`gpt-4o`, `gpt-4o-mini`)                                                                                    |
| Google Cloud     | Claude(`claude-3.7-sonnet`,`claude-3.5-sonnet`), Gemini(`gemini-2.0-flash`,`gemini-1.5-flash-*`,`gemini-2.0-pro-*`) |
