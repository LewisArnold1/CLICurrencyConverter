# CLI Currency Converter

A Python command-line tool for converting currencies using live exchange rate data from [exchangeratesapi.io](https://exchangeratesapi.io), with built-in support for offline use via cached rates.

## Features

- Convert between 168 world currencies using real-time exchange rates
- Offline mode using the last successfully fetched rates
- Automatic caching: every successful API call updates the local rates file
- Configurable logging with both console and file output
- Comprehensive test suite with 100% passing tests

## Requirements

- Python 3.12 or higher
- A free API key from [exchangeratesapi.io](https://manage.exchangeratesapi.io/signup/free)

## Installation

1. Clone the repository:
```shell
   git clone https://github.com/LewisArnold1/CLICurrencyConverter.git
   cd CLICurrencyConverter
```

2. Install dependencies using [uv](https://github.com/astral-sh/uv):
```shell
   uv sync
```

3. Create a `.env` file in the project root with your API key:
```
   EXCHANGE_RATE_API_KEY=your_api_key_here
```

## Usage

### Live conversion (requires internet)
```shell
python converter.py --base USD --target EUR --amount 100
```

### Offline conversion (uses cached rates)
```shell
python converter.py --base JPY --target GBP --amount 400 --mock
```

### With verbose logging
```shell
python converter.py --base USD --target EUR --amount 100 --log-level DEBUG
```

### Arguments

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--base` | `-b` | Source currency code (e.g. USD) | required |
| `--target` | `-t` | Target currency code (e.g. EUR) | required |
| `--amount` | `-a` | Amount to convert | required |
| `--mock` | `-m` | Use cached rates instead of live API | False |
| `--log-level` | `-l` | Console log level (DEBUG/INFO/WARNING/ERROR/CRITICAL) | INFO |

## Running Tests

Run the full test suite:
```shell
python -m pytest tests/ -v
```

## Project Structure

```
CLICurrencyConverter/
├── converter.py              # CLI entry point
├── src/
│   ├── api_client.py         # Fetches live rates from API
│   ├── cli.py                # Argument parsing
│   ├── converter.py          # Pure conversion logic
│   ├── logger_config.py      # Logging setup
│   └── rates_cache.py        # Reads/writes cached rates
├── tests/                    # Unit and integration tests
├── data/
│   └── last_rates.json       # Cached exchange rates
├── pyproject.toml            # Dependencies
└── .env                      # API key (not committed)
```

## Design Decisions

### Why EUR as the base for all rates?
The free tier of exchangeratesapi.io only returns rates with EUR as the base. All conversions between non-EUR currencies therefore use EUR as an intermediary (e.g. USD → EUR → GBP). The conversion logic is written to handle this transparently.

### Why auto-update the cache on every successful fetch?
Every live API call silently updates `data/last_rates.json`. This keeps the offline mode useful without requiring any extra steps from the user. The first time the tool is cloned, an initial `last_rates.json` ships with the repo so `--mock` works immediately.

### Why use the root logger pattern?
Logger configuration is applied to the root logger once at application startup, then all module-level loggers inherit from it. This allows the `--log-level` flag to take effect across the whole application from a single CLI argument, without each module needing to know how the user configured logging.

### Why is the conversion logic a pure function?
`convert_currency` takes rates as an argument rather than fetching them itself. This keeps it testable without any I/O mocking and clearly separates data retrieval from calculation.

### Why separate console and file logging?
The console shows messages relevant to the user (INFO and above by default, configurable via CLI), while the log file captures everything at DEBUG level for troubleshooting. Verbose third-party libraries like `urllib3` are suppressed to prevent API keys leaking into logs via request URLs.

## Branching Strategy

This project uses a feature-branch workflow:
- `main` contains the stable, working version at all times
- Each feature is developed on its own `feature/*` branch
- Changes are merged into `main` via self-approved pull requests

## License

This project is for educational purposes.