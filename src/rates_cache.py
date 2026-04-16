"""Module for loading and saving cached exchange rates."""

import json
import os

from src.logger_config import get_logger

logger = get_logger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
RATES_FILE = os.path.join(DATA_DIR, "last_rates.json")


def load_rates(file_path: str = RATES_FILE) -> dict:
    """
    Load exchange rates from a JSON file.

    Args:
        file_path (str): Path to the rates JSON file. Defaults to data/last_rates.json.

    Returns:
        dict: The parsed exchange rate data.

    Raises:
        FileNotFoundError: If the rates file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    logger.debug("Loading rates from %s", file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info("Successfully loaded rates dated %s", data.get("date", "unknown"))
    return data


def save_rates(data: dict, file_path: str = RATES_FILE) -> None:
    """
    Save exchange rate data to a JSON file.

    Args:
        data (dict): The exchange rate data to save.
        file_path (str): Path to the output file. Defaults to data/last_rates.json.

    Raises:
        OSError: If the file cannot be written (e.g. permission denied).
    """
    logger.debug("Saving rates to %s", file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    logger.info("Successfully saved rates dated %s", data.get("date", "unknown"))
