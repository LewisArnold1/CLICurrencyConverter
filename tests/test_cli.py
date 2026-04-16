"""Tests for the CLI module."""

import pytest

from src.cli import parse_args


@pytest.mark.parametrize(
    "argv, attribute, expected",
    [
        pytest.param(
            ["prog", "--base", "USD", "--target", "EUR", "--amount", "100"],
            "base", "USD",
            id="long flag base",
        ),
        pytest.param(
            ["prog", "--base", "USD", "--target", "EUR", "--amount", "100"],
            "target", "EUR",
            id="long flag target",
        ),
        pytest.param(
            ["prog", "--base", "USD", "--target", "EUR", "--amount", "100"],
            "amount", 100.0,
            id="long flag amount",
        ),
        pytest.param(
            ["prog", "-b", "USD", "-t", "EUR", "-a", "100"],
            "base", "USD",
            id="short flag base",
        ),
        pytest.param(
            ["prog", "-b", "USD", "-t", "EUR", "-a", "100"],
            "target", "EUR",
            id="short flag target",
        ),
        pytest.param(
            ["prog", "-b", "USD", "-t", "EUR", "-a", "100"],
            "amount", 100.0,
            id="short flag amount",
        ),
        pytest.param(
            ["prog", "-b", "USD", "-t", "EUR", "-a", "100", "--mock"],
            "mock", True,
            id="mock flag present",
        ),
        pytest.param(
            ["prog", "-b", "USD", "-t", "EUR", "-a", "100"],
            "mock", False,
            id="mock flag absent defaults to False",
        ),
        pytest.param(
            ["prog", "-b", "USD", "-t", "EUR", "-a", "100"],
            "log_level", "INFO",
            id="log level defaults to INFO",
        ),
        pytest.param(
            ["prog", "-b", "USD", "-t", "EUR", "-a", "100", "--log-level", "DEBUG"],
            "log_level", "DEBUG",
            id="log level custom",
        ),
    ],
)
def test_parse_args_valid_inputs(monkeypatch, argv, attribute, expected):
    """Test that valid CLI arguments produce the expected parsed attributes."""
    monkeypatch.setattr("sys.argv", argv)

    args = parse_args()

    assert getattr(args, attribute) == expected


@pytest.mark.parametrize(
    "argv",
    [
        pytest.param(
            ["prog", "--base", "USD"],
            id="missing required arguments",
        ),
        pytest.param(
            ["prog", "-b", "USD", "-t", "EUR", "-a", "abc"],
            id="non-numeric amount",
        ),
        pytest.param(
            ["prog", "-b", "USD", "-t", "EUR", "-a", "100", "--log-level", "INVALID"],
            id="invalid log level",
        ),
    ],
)
def test_parse_args_invalid_inputs(monkeypatch, argv):
    """Test that SystemExit is raised for invalid CLI input."""
    monkeypatch.setattr("sys.argv", argv)

    with pytest.raises(SystemExit):
        parse_args()
