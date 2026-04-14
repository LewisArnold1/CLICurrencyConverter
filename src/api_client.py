"""Module for fetching exchange rates from the exchangeratesapi.io API."""

import os

import requests
from dotenv import load_dotenv

from src.logger_config import get_logger
from src.rates_cache import save_rates

load_dotenv()

logger = get_logger(__name__)

BASE_URL = "http://api.exchangeratesapi.io/v1/latest"


def fetch_rates() -> dict:
    """
    Fetch the latest exchange rates from the API.

    Rates are returned with EUR as the base currency.
    On success, the cached rates file is automatically updated.

    Returns:
        dict: The API response containing exchange rate data.

    Raises:
        ValueError: If the API key is not set.
        requests.exceptions.RequestException: If the API request fails.
        ValueError: If the API returns an unsuccessful response.
    """
    api_key = os.environ.get("EXCHANGE_RATE_API_KEY")

    if not api_key:
        logger.error("API key not found in environment variables")
        raise ValueError("EXCHANGE_RATE_API_KEY environment variable is not set")

    logger.debug("Fetching rates from API")

    response = requests.get(BASE_URL, params={"access_key": api_key}, timeout=10)
    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        error_info = data.get("error", {})
        logger.error("API returned error: %s", error_info)
        raise ValueError(f"API error: {error_info}")

    logger.info("Successfully fetched rates dated %s", data.get("date"))

    save_rates(data)

    return data
