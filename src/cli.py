"""Module for parsing command line arguments."""

import argparse


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments for the currency converter.

    Returns:
        argparse.Namespace: Parsed arguments containing base, target,
            amount, mock, and log_level.
    """
    parser = argparse.ArgumentParser(
        description="Convert currencies using live or cached exchange rates."
    )

    parser.add_argument(
        "--base", "-b",
        required=True,
        help="Base currency code (e.g. USD)",
    )

    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Target currency code (e.g. EUR)",
    )

    parser.add_argument(
        "--amount", "-a",
        type=float,
        required=True,
        help="Amount to convert",
    )

    parser.add_argument(
        "--mock", "-m",
        action="store_true",
        default=False,
        help="Use cached rates instead of live API data",
    )

    parser.add_argument(
        "--log-level", "-l",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the console logging level (default: INFO)",
    )

    return parser.parse_args()
