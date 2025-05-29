from pydantic import BaseModel, ConfigDict, Field, field_validator


class CorePrompt(BaseModel):
    """Prompt class for core functionalities."""

    judge_document_type: str = Field(description="Prompt for judging document type.")
    extract_document: str = Field(
        description="Prompt for extracting document content.",
    )
    update_context: str = Field(
        description="Prompt for updating context.",
    )

    # Prompt for different document types
    table_prompt: str = Field(
        description="Prompt for extracting table data.",
    )
    flowchart_prompt: str = Field(
        description="Prompt for extracting flowchart data.",
    )
    graph_prompt: str = Field(
        description="Prompt for extracting graph data.",
    )
    image_prompt: str = Field(
        description="Prompt for extracting image data.",
    )

    extract_document_text_prompt: str = Field(
        description="Prompt for extracting text from a document.",
    )
    extract_image_only_prompt: str = Field(description="Prompt for extracting text from an image.")

    def extract_human_message(self, document_text: str) -> str:
        """Generates a human message based on the document text and image."""
        return (
            self.extract_document_text_prompt.format(document_text=document_text)
            if document_text
            else self.extract_image_only_prompt.format(document_text=document_text)
        )

    @field_validator("judge_document_type")
    def validate_judge_document_type(cls, value):
        if "{types_explanation}" not in value:
            raise ValueError("The string must contain '{types_explanation}'.")
        elif "{format_instructions}" not in value:
            raise ValueError("The string must contain '{format_instructions}'.")
        return value

    @field_validator("extract_document")
    def validate_extract_document(cls, value):
        if "{document_type_prompt}" not in value:
            raise ValueError("The string must contain '{document_type_prompt}'.")
        elif "{context}" not in value:
            raise ValueError("The string must contain '{context}'.")
        elif "{format_instruction}" not in value:
            raise ValueError("The string must contain '{format_instruction}'.")
        return value

    @field_validator("update_context")
    def validate_update_context(cls, value):
        if "{context}" not in value:
            raise ValueError("The string must contain '{context}'.")
        elif "{format_instructions}" not in value:
            raise ValueError("The string must contain '{format_instructions}'.")
        return value

    @field_validator("extract_document_text_prompt")
    def validate_extract_document_text_prompt(cls, value):
        if "{document_text}" not in value:
            raise ValueError("The string must contain '{document_text}'.")
        return value

    model_config = ConfigDict(frozen=True)
