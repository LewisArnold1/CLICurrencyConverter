"""Tests for the logger configuration module."""

import logging
import pytest

from src.logger_config import configure_logging, get_logger


@pytest.fixture(autouse=True)
def reset_root_logger():
    """Reset the root logger before each test."""
    root = logging.getLogger()
    root.handlers.clear()
    yield
    root.handlers.clear()


def test_configure_logging_sets_two_handlers(tmp_path):
    """Test that configure_logging adds a StreamHandler and FileHandler."""
    log_file = tmp_path / "test.log"

    configure_logging(log_file=str(log_file))

    root = logging.getLogger()
    assert len(root.handlers) == 2


def test_configure_logging_handler_types(tmp_path):
    """Test that both handler types are present."""
    log_file = tmp_path / "test.log"

    configure_logging(log_file=str(log_file))

    root = logging.getLogger()
    handler_types = [type(h) for h in root.handlers]
    assert logging.StreamHandler in handler_types
    assert logging.FileHandler in handler_types


def test_configure_logging_console_level_default(tmp_path):
    """Test that console level defaults to INFO."""
    log_file = tmp_path / "test.log"

    configure_logging(log_file=str(log_file))

    root = logging.getLogger()
    stream_handler = [h for h in root.handlers if type(h) is logging.StreamHandler][0]
    assert stream_handler.level == logging.INFO


def test_configure_logging_console_level_custom(tmp_path):
    """Test that a custom console level is respected."""
    log_file = tmp_path / "test.log"

    configure_logging(log_file=str(log_file), console_level="WARNING")

    root = logging.getLogger()
    stream_handler = [h for h in root.handlers if type(h) is logging.StreamHandler][0]
    assert stream_handler.level == logging.WARNING


def test_configure_logging_file_is_created(tmp_path):
    """Test that the log file is created when a message is logged."""
    log_file = tmp_path / "test.log"

    configure_logging(log_file=str(log_file))
    logging.getLogger("test").info("hello")

    assert log_file.exists()


def test_configure_logging_clears_previous_handlers(tmp_path):
    """Test that reconfiguring replaces old handlers rather than appending."""
    log_file = tmp_path / "test.log"

    configure_logging(log_file=str(log_file))
    configure_logging(log_file=str(log_file))

    root = logging.getLogger()
    assert len(root.handlers) == 2


def test_get_logger_returns_logger_instance():
    """Test that get_logger returns a Logger."""
    logger = get_logger("test_module")
    assert isinstance(logger, logging.Logger)
