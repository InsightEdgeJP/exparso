from .prompt import CorePrompt

JAPANESE_CORE_PROMPT = CorePrompt(
    judge_document_type="""Analyze the input image and classify its content according to the following properties.
# Steps

1. Analyze the input image to identify all content types present.
2. For each property, select all that apply.

# Types
{types_explanation}

# Output Format
{format_instructions}
""",  # noqa
    extract_document="""あなたは画像から文書を読み取る専門家です。与えられた画像の内容を正確に書き起こしてください。

# Constraints

- ユーザーが文章を入力します。ドキュメントをより正確にするために修正してください。
- 画像に存在しない内容は回答しないでください。
- Document Type はデータを読み込みときの参考情報として提供されます。
- Document Context はドキュメントの参考情報として提供されます。
- 出力は {format_instruction} で指定された JSON のみを返してください。前後に説明や余分なテキストを追加しないでください。

# Document Type

## Text

- 画像内のすべてのテキストを正しく抽出してください。

{document_type_prompt}

# Document Context

{context}

# Output
{format_instruction}
""",  # noqa
    update_context="""提供されたコンテキストと新しい情報に基づいて、コンテキストを更新してください。

# Constraints

- 新しい要件、前提条件、またはアクション項目をリストにしてください。これは、今後の処理で必要になる可能性があります。
- 新しい情報はユーザー入力によって提供されます。
- コンテキストは5〜7文で維持してください。
 
# Context

{context}

# Example

応募者は申請前に少なくとも1年間その州に居住している必要があります。
必要書類には有効な運転免許証または州発行のIDが含まれます。
応募者は18歳以上でなければなりません。
所得証明書（最近の給与明細または納税申告書）が必要です。
応募者は最終承認前に必須のトレーニングセッションを完了しなければなりません。

# Output
{format_instructions}
""",  # noqa
    table_prompt="""
## Table

- まずテーブル全体の概要（目的、期間、レコード数など）を2〜3文で記述してください。
- 続けて、注目すべき指標・傾向・外れ値・欠損値・比較関係などの洞察を箇条書きで列挙してください。
- 最後に、入力データをマークダウン形式の表として再掲してください。列の順序は元データに合わせてください。

### Example
**Input**: 名前と年齢が含まれるテーブル。
**Output**:
このテーブルは2人の名前と年齢を示しており、Alice が最年少 (25)、Bob が30歳です。
- Alice は25歳でエンジニアです。
- Bob は30歳でデザイナーです。

| Name  | Age | Occupation |
|-------|-----|------------|
| Alice | 25  | Engineer   |
| Bob   | 30  | Designer   |

""",
    flowchart_prompt="""
## Flowchart

- フローチャートの情報を説明してください。
- フローチャートをMermaid形式に変換してください。
- 出力にフローチャートの概要を追加してください。

### Example
**Input**: ケーキ作りのプロセスを示すフローチャート。
**Output**:
このフローチャートはケーキ作りのプロセスを示しています。
```mermaid
graph TD;
    A(Start) --> B(Add flour)
    B --> C(Add sugar)
    C --> D(Bake)
    D --> E(End)
```

""",
    graph_prompt="""
## Graph

- グラフ内の情報を説明してください。
- グラフ内のテキストを読み取り、内容を記述してください。
- 出力にグラフの概要を追加してください。

### Example
**Input**: 人数と車の数が含まれるグラフ。
**Output**:
このグラフは人数と車の数の関係を示しています。
人数が増加している一方、車の数は減少しています。
2020年には、人数が100人で、車の数が50台です。

""",
    image_prompt="""
## Image

- 画像内の情報を説明してください。
- 画像にテキストが含まれている場合、その内容を記述してください。

### Example
**Input**: 異なるセクションを説明するラベルが付いた円グラフが含まれる画像。
**Output**:
この画像は、異なるセクションを説明するラベルが付いた円グラフを示しています。
最も大きなセクションはAで、続いてBとCが続きます。

""",
    extract_document_text_prompt="以下のテキストを読み取りました。\n {document_text}",
    extract_image_only_prompt="入力は画像のみです。",
)

ENGLISH_CORE_PROMPT = CorePrompt(
    judge_document_type="""Analyze the input image and classify its content according to the following properties.
# Steps

1. Analyze the input image to identify all content types present.
2. For each property, select all that apply.

# Types
{types_explanation}

# Output Format
{format_instructions}
""",  # noqa
    extract_document="""You are an expert in reading documents from images.
Please write out the content accurately, staying faithful to the given image content.

# Constraints
- User will input the sentence. Please modify the sentence to make it more accurate.
- Don't hallucinate the content that doesn't exist in the image.
- Document Text is provided for reference.
- Document Context is provided for reference.
- Respond strictly with the JSON specified by {format_instruction}. Do not prepend or append any prose outside the JSON.

# Document Type

## Text

- Please extract the all texts in this documents.

{document_type_prompt}

# Document Context

{context}

# Output
{format_instruction}
""",  # noqa
    update_context="""Based on the provided context and new information, update the context to include relevant information.

# Constraints
- List any requirements, prerequisites, or action items extracted from new information, as they may be necessary for further pages.
- New information is provided by user input.
- Maintain the context with 5-7 sentences.

# Context

{context}

# Example

The applicant must be a resident of the state for at least one year before applying.
Required documents include a valid driver’s license or state ID.
The applicant must be at least 18 years old.
Proof of income (recent pay stubs or tax returns) is required.
A mandatory training session must be completed by the applicant before final approval.

# Output
{format_instructions}
""",  # noqa
    table_prompt="""
## Table

- Start with 2-3 sentences summarizing what the table represents (goal, timeframe, number of records, etc.).
- Follow with bullet points that highlight notable metrics, trends, outliers, missing values, or comparisons between rows/columns.
- Reproduce the data as a Markdown table at the end. Preserve the original column order.

### Example

**Input**: A table contains the age, name, and occupation.
**Output**:
This table lists two people along with their ages and occupations. Alice is younger (25) than Bob (30).
- Alice is a 25-year-old engineer.
- Bob is a 30-year-old designer.

| Name  | Age | Occupation |
|-------|-----|------------|
| Alice | 25  | Engineer   |
| Bob   | 30  | Designer   |

""",
    flowchart_prompt="""
## Flowchart

- Please describe the information in the flowchart.
- Translate the flowchart into mermaid format.
- Add summary of the flowchart in the output.

### Example
**Input**: A flowchart contains the process of making a cake.
**Output**:
This flowchart shows the process of making a cake.
```mermaid
graph TD;
    A(Start) --> B(Add flour)
    B --> C(Add sugar)
    C --> D(Bake)
    D --> E(End)
```

""",
    graph_prompt="""
## Graph

- Please describe the information in the graph.
- Read the text in the graph and describe the content.
- Add summary of the graph in the output.

### Example
**Input**: A graph contains the number of people and the number of cars.
**Output**:
This graph shows the relationship between the number of people and the number of cars.
The number of people is increasing, while the number of cars is decreasing.
In 2020, the number of people is 100, and the number of cars is 50.

""",
    image_prompt="""
## Image

- Please describe the information in the image.
- If the image contains text, please describe the content.

### Example
**Input**: An image contains a pie chart with labels describing different sections.
**Output**:
This image shows a pie chart with labels describing different sections.
The largest section is A, followed by B and C.

""",  # noqa
    extract_document_text_prompt="I have read the following text.\n {document_text}",
    extract_image_only_prompt="The input is an image only.",
)
