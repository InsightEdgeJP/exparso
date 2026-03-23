import logging
from pathlib import Path

from exparso import parse_document
from exparso import _DEPENDENCY_LOGGER_NAMESPACES


LOGGER_NAMESPACES = ("exparso", *_DEPENDENCY_LOGGER_NAMESPACES)


class _DummyLoader:
    def load(self, path: str) -> list[object]:
        return []


def _reset_logger_levels() -> dict[str, int]:
    original_levels: dict[str, int] = {}
    for namespace in LOGGER_NAMESPACES:
        logger = logging.getLogger(namespace)
        original_levels[namespace] = logger.level
        logger.setLevel(logging.NOTSET)
    return original_levels


def _restore_logger_levels(original_levels: dict[str, int]) -> None:
    for namespace, level in original_levels.items():
        logging.getLogger(namespace).setLevel(level)


def test_parse_document_sets_exparso_log_level(monkeypatch):
    original_levels = _reset_logger_levels()
    monkeypatch.setattr("exparso.LoaderFactory.create", lambda extension: _DummyLoader())
    monkeypatch.setattr("exparso.LlmFactory.create", lambda model: None)

    try:
        parse_document(str(Path(__file__)), log_level=logging.ERROR)
        exparso_level = logging.getLogger("exparso").level
        pdfminer_level = logging.getLogger("pdfminer").level
    finally:
        _restore_logger_levels(original_levels)

    assert exparso_level == logging.ERROR
    assert pdfminer_level == logging.NOTSET


def test_parse_document_sets_dependency_log_levels(monkeypatch):
    original_levels = _reset_logger_levels()
    monkeypatch.setattr("exparso.LoaderFactory.create", lambda extension: _DummyLoader())
    monkeypatch.setattr("exparso.LlmFactory.create", lambda model: None)

    try:
        parse_document(str(Path(__file__)), log_level=logging.ERROR, include_dependency_logs=True)
        current_levels = {namespace: logging.getLogger(namespace).level for namespace in LOGGER_NAMESPACES}
    finally:
        _restore_logger_levels(original_levels)

    for namespace in LOGGER_NAMESPACES:
        assert current_levels[namespace] == logging.ERROR


def test_parse_document_does_not_change_log_level_when_not_specified(monkeypatch):
    original_levels = _reset_logger_levels()
    monkeypatch.setattr("exparso.LoaderFactory.create", lambda extension: _DummyLoader())
    monkeypatch.setattr("exparso.LlmFactory.create", lambda model: None)

    try:
        parse_document(str(Path(__file__)))
    finally:
        current_levels = {namespace: logging.getLogger(namespace).level for namespace in LOGGER_NAMESPACES}
        _restore_logger_levels(original_levels)

    assert current_levels == {namespace: logging.NOTSET for namespace in LOGGER_NAMESPACES}
