"""Module for configuring logging across the application."""

import logging

# Suppress verbose third-party DEBUG logs
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


def configure_logging(
    log_file: str = "currency_converter.log",
    console_level: str = "INFO",
    file_level: str = "DEBUG",
) -> None:
    """
    Configure the root logger. Should be called once at application startup.

    All loggers created via get_logger inherit from this configuration.
    Calling this function again clears and replaces any existing handlers.

    Args:
        log_file (str): Path to the log file. Defaults to 'currency_converter.log'.
        console_level (str): Console handler level. Must be one of DEBUG, INFO,
            WARNING, ERROR, CRITICAL. Defaults to 'INFO'.
        file_level (str): File handler level. Must be one of DEBUG, INFO,
            WARNING, ERROR, CRITICAL. Defaults to 'DEBUG'.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel("DEBUG")

    # Clear any existing handlers
    root_logger.handlers.clear()

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(console_level.upper())
    stream_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(file_level.upper())
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s")
    )

    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for the given name. Inherits config from root logger.

    Args:
        name (str): Name of the logger, typically __name__.

    Returns:
        logging.Logger: A logger instance.
    """
    return logging.getLogger(name)
