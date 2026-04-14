"""Module for converting between currencies."""

from src.logger_config import get_logger

logger = get_logger(__name__)


def convert_currency(
    base: str, target: str, amount: float, rates: dict
) -> float:
    """
    Convert an amount from one currency to another.

    All rates are relative to EUR. If neither base nor target is EUR,
    the conversion is done via EUR as an intermediary.

    Args:
        base (str): The source currency code (e.g. 'USD').
        target (str): The target currency code (e.g. 'GBP').
        amount (float): The amount to convert.
        rates (dict): Exchange rates dictionary with EUR as base.

    Returns:
        float: The converted amount, rounded to 2 decimal places.

    Raises:
        ValueError: If base or target currency is not found in rates.
    """
    base = base.upper()
    target = target.upper()

    logger.debug("Converting %s %s to %s", amount, base, target)

    if base == target:
        logger.info("Base and target are the same, returning original amount")
        return round(amount, 2)

    if base != "EUR" and base not in rates:
        raise ValueError(f"Unsupported currency: {base}")

    if target != "EUR" and target not in rates:
        raise ValueError(f"Unsupported currency: {target}")

    # Convert base to EUR first
    if base == "EUR":
        amount_in_eur = amount
    else:
        amount_in_eur = amount / rates[base]

    # Convert EUR to target
    if target == "EUR":
        result = amount_in_eur
    else:
        result = amount_in_eur * rates[target]

    logger.info("Converted %s %s to %.2f %s", amount, base, result, target)
    return round(result, 2)
