# pylint: disable=redefined-outer-name, unused-argument
"""Tests for the main entry point."""

import pytest
import requests

from converter import main


@pytest.fixture
def mock_rates_data():
    """Provide sample rates data returned by fetch_rates or load_rates."""
    return {
        "success": True,
        "base": "EUR",
        "date": "2026-04-14",
        "rates": {"USD": 1.18, "GBP": 0.87, "JPY": 130.0},
    }


@pytest.fixture
def mock_successful_fetch(monkeypatch, mock_rates_data):
    """Mock a successful fetch_rates call."""
    monkeypatch.setattr("converter.fetch_rates", lambda: mock_rates_data)


@pytest.fixture
def mock_successful_load(monkeypatch, mock_rates_data):
    """Mock a successful load_rates call."""
    monkeypatch.setattr("converter.load_rates", lambda: mock_rates_data)


def test_main_live_mode_prints_result(monkeypatch, capsys, mock_successful_fetch):
    """Test that live mode prints the converted amount."""
    monkeypatch.setattr(
        "sys.argv",
        ["converter.py", "--base", "USD", "--target", "GBP", "--amount", "100"],
    )

    main()

    captured = capsys.readouterr()
    assert "USD" in captured.out
    assert "GBP" in captured.out


def test_main_mock_mode_prints_result(monkeypatch, capsys, mock_successful_load):
    """Test that mock mode prints the converted amount."""
    monkeypatch.setattr(
        "sys.argv",
        ["converter.py", "--base", "JPY", "--target", "GBP", "--amount", "400", "--mock"],
    )

    main()

    captured = capsys.readouterr()
    assert "JPY" in captured.out
    assert "GBP" in captured.out


def test_main_mock_mode_does_not_call_api(monkeypatch, capsys, mock_successful_load):
    """Test that mock mode does not trigger fetch_rates."""
    def raise_if_called():
        raise AssertionError("fetch_rates should not be called in mock mode")

    monkeypatch.setattr("converter.fetch_rates", raise_if_called)
    monkeypatch.setattr(
        "sys.argv",
        ["converter.py", "--base", "USD", "--target", "GBP", "--amount", "100", "--mock"],
    )

    main()


def test_main_missing_cache_file_exits(monkeypatch):
    """Test that main exits with code 1 when cache file is missing in mock mode."""
    def raise_file_not_found():
        raise FileNotFoundError()

    monkeypatch.setattr("converter.load_rates", raise_file_not_found)
    monkeypatch.setattr(
        "sys.argv",
        ["converter.py", "--base", "USD", "--target", "GBP", "--amount", "100", "--mock"],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1


def test_main_network_error_exits(monkeypatch):
    """Test that main exits with code 1 on network error."""
    def raise_connection_error():
        raise requests.exceptions.ConnectionError("Network unreachable")

    monkeypatch.setattr("converter.fetch_rates", raise_connection_error)
    monkeypatch.setattr(
        "sys.argv",
        ["converter.py", "--base", "USD", "--target", "GBP", "--amount", "100"],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1


def test_main_invalid_currency_exits(monkeypatch, mock_successful_fetch):
    """Test that main exits with code 1 when conversion fails."""
    monkeypatch.setattr(
        "sys.argv",
        ["converter.py", "--base", "XYZ", "--target", "GBP", "--amount", "100"],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
