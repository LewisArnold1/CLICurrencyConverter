"""Tests for the logger configuration module."""

import logging
from src.logger_config import get_logger


def test_get_logger_returns_logger_instance():
    """Test that get_logger returns a logging.Logger object."""
    logger = get_logger("test_instance")
    
    assert isinstance(logger, logging.Logger)


def test_get_logger_has_two_handlers():
    """Test that the logger has both a StreamHandler and a FileHandler."""
    logger = get_logger("test_handlers")

    assert len(logger.handlers) == 2


def test_get_logger_handler_types():
    """Test that the logger has the correct handler types."""
    logger = get_logger("test_handler_types")
    handler_types = [type(h) for h in logger.handlers]

    assert logging.StreamHandler in handler_types
    assert logging.FileHandler in handler_types


def test_get_logger_console_level_default():
    """Test that the StreamHandler defaults to INFO level."""
    logger = get_logger("test_console_default")
    stream_handler = [h for h in logger.handlers if type(h) is logging.StreamHandler][0]

    assert stream_handler.level == logging.INFO


def test_get_logger_console_level_custom():
    """Test that the StreamHandler respects a custom console level."""
    logger = get_logger("test_console_custom", console_level="WARNING")
    stream_handler = [h for h in logger.handlers if type(h) is logging.StreamHandler][0]

    assert stream_handler.level == logging.WARNING


def test_get_logger_file_created(tmp_path):
    """Test that the log file is created when the logger is used."""
    log_file = tmp_path / "test.log"
    logger = get_logger("test_file_creation", log_file=str(log_file))
    logger.info("test message")

    assert log_file.exists()


def test_get_logger_no_duplicate_handlers():
    """Test that calling get_logger twice does not add duplicate handlers."""
    logger = get_logger("test_no_duplicates")
    handler_count_first = len(logger.handlers)
    get_logger("test_no_duplicates")

    assert len(logger.handlers) == handler_count_first
