"""Module for configuring logging across the application."""

import logging


def get_logger(
    name: str,
    log_file: str = "currency_converter.log",
    console_level: str = "INFO",
    file_level: str = "DEBUG",
) -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name (str): Name of logger.
        log_file (str): Path to the log file. Defaults to 'currency_converter.log'.
        console_level (str): Logging level for console output. Defaults to 'INFO'.
        file_level (str): Logging level for file output. Defaults to 'DEBUG'.

    Returns:
        logging.Logger: A logger instance with a StreamHandler and a FileHandler.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent adding duplicate handlers if get_logger is called multiple times
    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(console_level.upper())

        stream_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler.setFormatter(stream_formatter)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(file_level.upper())

        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger
