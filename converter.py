"""Entry point for the CLI currency converter."""

import sys

import requests

from src.api_client import fetch_rates
from src.cli import parse_args
from src.converter import convert_currency
from src.logger_config import get_logger
from src.rates_cache import load_rates


def main() -> None:
    """Run the currency converter based on command line arguments."""
    args = parse_args()

    logger = get_logger(__name__, console_level=args.log_level)

    try:
        if args.mock:
            logger.info("Using cached rates (mock mode)")
            data = load_rates()
        else:
            logger.info("Fetching live rates from API")
            data = fetch_rates()

        result = convert_currency(args.base, args.target, args.amount, data["rates"])

        print(f"{args.amount} {args.base.upper()} = {result} {args.target.upper()}")

    except FileNotFoundError:
        logger.error("No cached rates available. Run without --mock first.")
        sys.exit(1)
    except ValueError as e:
        logger.error("%s", e)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logger.error("Network error: %s. Try running with --mock.", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
