import pytest
from pydantic import ValidationError

from exparso.core.prompt.prompt import CorePrompt


def test_core_prompt_valid():
    """Test creating a valid CorePrompt instance."""
    judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
    extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
    update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    prompt = CorePrompt(
        judge_document_type=judge_doc_type,
        extract_document=extract_doc,
        update_context=update_ctx,
        table_prompt="Table prompt",
        flowchart_prompt="Flowchart prompt",
        graph_prompt="Graph prompt",
        image_prompt="Image prompt",
        extract_document_text_prompt=extract_doc_text,
        extract_image_only_prompt=extract_img_only,
    )
    # Check judge_document_type placeholders
    assert "{types_explanation}" in prompt.judge_document_type
    assert "{format_instructions}" in prompt.judge_document_type

    # Check extract_document placeholders
    assert "{document_type_prompt}" in prompt.extract_document
    assert "{context}" in prompt.extract_document
    assert "{format_instruction}" in prompt.extract_document

    # Check update_context placeholders
    assert "{context}" in prompt.update_context
    assert "{format_instructions}" in prompt.update_context

    # Check extract_document_text_prompt placeholder
    assert "{document_text}" in prompt.extract_document_text_prompt


def test_judge_document_type_missing_types_explanation():
    """Test validation error when {types_explanation} is missing in judge_document_type."""
    extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
    update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    with pytest.raises(ValidationError) as excinfo:
        CorePrompt(
            judge_document_type="Format: {format_instructions}",
            extract_document=extract_doc,
            update_context=update_ctx,
            table_prompt="Table prompt",
            flowchart_prompt="Flowchart prompt",
            graph_prompt="Graph prompt",
            image_prompt="Image prompt",
            extract_document_text_prompt=extract_doc_text,
            extract_image_only_prompt=extract_img_only,
        )

    # Check that the error message contains the expected text
    error_msg = str(excinfo.value)
    assert "The string must contain '{types_explanation}'" in error_msg


def test_judge_document_type_missing_format_instructions():
    """Test validation error when {format_instructions} is missing in judge_document_type."""
    extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
    update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    with pytest.raises(ValidationError) as excinfo:
        CorePrompt(
            judge_document_type="Types: {types_explanation}",
            extract_document=extract_doc,
            update_context=update_ctx,
            table_prompt="Table prompt",
            flowchart_prompt="Flowchart prompt",
            graph_prompt="Graph prompt",
            image_prompt="Image prompt",
            extract_document_text_prompt=extract_doc_text,
            extract_image_only_prompt=extract_img_only,
        )

    # Check that the error message contains the expected text
    error_msg = str(excinfo.value)
    assert "The string must contain '{format_instructions}'" in error_msg


def test_extract_document_missing_document_type_prompt():
    """Test validation error when {document_type_prompt} is missing in extract_document."""
    judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
    update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    with pytest.raises(ValidationError) as excinfo:
        CorePrompt(
            judge_document_type=judge_doc_type,
            extract_document="Context: {context}\nFormat: {format_instruction}",
            update_context=update_ctx,
            table_prompt="Table prompt",
            flowchart_prompt="Flowchart prompt",
            graph_prompt="Graph prompt",
            image_prompt="Image prompt",
            extract_document_text_prompt=extract_doc_text,
            extract_image_only_prompt=extract_img_only,
        )

    # Check that the error message contains the expected text
    error_msg = str(excinfo.value)
    assert "The string must contain '{document_type_prompt}'" in error_msg


def test_extract_document_missing_context():
    """Test validation error when {context} is missing in extract_document."""
    judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
    update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    with pytest.raises(ValidationError) as excinfo:
        CorePrompt(
            judge_document_type=judge_doc_type,
            extract_document="Document type: {document_type_prompt}\nFormat: {format_instruction}",
            update_context=update_ctx,
            table_prompt="Table prompt",
            flowchart_prompt="Flowchart prompt",
            graph_prompt="Graph prompt",
            image_prompt="Image prompt",
            extract_document_text_prompt=extract_doc_text,
            extract_image_only_prompt=extract_img_only,
        )

    # Check that the error message contains the expected text
    error_msg = str(excinfo.value)
    assert "The string must contain '{context}'" in error_msg


def test_extract_document_missing_format_instruction():
    """Test validation error when {format_instruction} is missing in extract_document."""
    judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
    update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    with pytest.raises(ValidationError) as excinfo:
        CorePrompt(
            judge_document_type=judge_doc_type,
            extract_document="Document type: {document_type_prompt}\nContext: {context}",
            update_context=update_ctx,
            table_prompt="Table prompt",
            flowchart_prompt="Flowchart prompt",
            graph_prompt="Graph prompt",
            image_prompt="Image prompt",
            extract_document_text_prompt=extract_doc_text,
            extract_image_only_prompt=extract_img_only,
        )

    # Check that the error message contains the expected text
    error_msg = str(excinfo.value)
    assert "The string must contain '{format_instruction}'" in error_msg


def test_update_context_missing_context():
    """Test validation error when {context} is missing in update_context."""
    judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
    extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    with pytest.raises(ValidationError) as excinfo:
        CorePrompt(
            judge_document_type=judge_doc_type,
            extract_document=extract_doc,
            update_context="Format instructions: {format_instructions}",
            table_prompt="Table prompt",
            flowchart_prompt="Flowchart prompt",
            graph_prompt="Graph prompt",
            image_prompt="Image prompt",
            extract_document_text_prompt=extract_doc_text,
            extract_image_only_prompt=extract_img_only,
        )

    # Check that the error message contains the expected text
    error_msg = str(excinfo.value)
    assert "The string must contain '{context}'" in error_msg


def test_update_context_missing_format_instructions():
    """Test validation error when {format_instructions} is missing in update_context."""
    judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
    extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    with pytest.raises(ValidationError) as excinfo:
        CorePrompt(
            judge_document_type=judge_doc_type,
            extract_document=extract_doc,
            update_context="Here is the context: {context}",
            table_prompt="Table prompt",
            flowchart_prompt="Flowchart prompt",
            graph_prompt="Graph prompt",
            image_prompt="Image prompt",
            extract_document_text_prompt=extract_doc_text,
            extract_image_only_prompt=extract_img_only,
        )

    # Check that the error message contains the expected text
    error_msg = str(excinfo.value)
    assert "The string must contain '{format_instructions}'" in error_msg


def test_extract_document_text_prompt_missing_document_text():
    """Test validation error when {document_text} is missing in extract_document_text_prompt."""
    judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
    extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
    update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
    extract_img_only = "Image only document"

    with pytest.raises(ValidationError) as excinfo:
        CorePrompt(
            judge_document_type=judge_doc_type,
            extract_document=extract_doc,
            update_context=update_ctx,
            table_prompt="Table prompt",
            flowchart_prompt="Flowchart prompt",
            graph_prompt="Graph prompt",
            image_prompt="Image prompt",
            extract_document_text_prompt="Missing document text placeholder",
            extract_image_only_prompt=extract_img_only,
        )

    # Check that the error message contains the expected text
    error_msg = str(excinfo.value)
    assert "The string must contain '{document_text}'" in error_msg


def test_extract_human_message():
    """Test the extract_human_message method."""
    judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
    extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
    update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    prompt = CorePrompt(
        judge_document_type=judge_doc_type,
        extract_document=extract_doc,
        update_context=update_ctx,
        table_prompt="Table prompt",
        flowchart_prompt="Flowchart prompt",
        graph_prompt="Graph prompt",
        image_prompt="Image prompt",
        extract_document_text_prompt=extract_doc_text,
        extract_image_only_prompt=extract_img_only,
    )

    # Test with document text
    document_text = "Sample document text"
    message = prompt.extract_human_message(document_text)
    assert document_text in message
    assert message == extract_doc_text.format(document_text=document_text)

    # Test with empty document text
    empty_document_text = ""
    message = prompt.extract_human_message(empty_document_text)
    assert message == extract_img_only.format(document_text=empty_document_text)


def test_model_is_frozen():
    """Test that the model is frozen (immutable)."""
    judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
    extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
    update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
    extract_doc_text = "Here is the document text: {document_text}"
    extract_img_only = "Image only document"

    prompt = CorePrompt(
        judge_document_type=judge_doc_type,
        extract_document=extract_doc,
        update_context=update_ctx,
        table_prompt="Table prompt",
        flowchart_prompt="Flowchart prompt",
        graph_prompt="Graph prompt",
        image_prompt="Image prompt",
        extract_document_text_prompt=extract_doc_text,
        extract_image_only_prompt=extract_img_only,
    )

    # Attempting to modify the model should raise an error
    # Pydantic v2 raises ValidationError for frozen instances
    with pytest.raises(Exception) as excinfo:
        prompt.table_prompt = "New table prompt"

    # Check that the error message indicates the instance is frozen
    assert "frozen" in str(excinfo.value).lower()
