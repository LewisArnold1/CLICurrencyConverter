# pylint: disable=redefined-outer-name, unused-argument, too-few-public-methods
"""Tests for the API client module."""

import pytest
import requests

from src.api_client import fetch_rates


@pytest.fixture
def mock_successful_response(monkeypatch):
    """Mock a successful API response."""
    class MockResponse:
        """Simulates a successful HTTP response from the exchange rates API."""
        status_code = 200

        def json(self):
            """Return sample exchange rate data."""
            return {
                "success": True,
                "timestamp": 1776159733,
                "base": "EUR",
                "date": "2026-04-14",
                "rates": {"USD": 1.18, "GBP": 0.87},
            }

        def raise_for_status(self):
            """Do nothing as the response is successful."""

    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "fake_key_for_testing")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())


@pytest.fixture
def mock_failed_response(monkeypatch):
    """Mock an unsuccessful API response."""
    class MockResponse:
        """Simulates an API response indicating an error."""
        status_code = 200

        def json(self):
            """Return an error response from the API."""
            return {
                "success": False,
                "error": {"code": 101, "type": "missing_access_key"},
            }

        def raise_for_status(self):
            """Do nothing as the HTTP request itself succeeded."""

    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "fake_key_for_testing")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())


@pytest.fixture
def mock_network_error(monkeypatch):
    """Mock a network error during the API request."""
    def raise_connection_error(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Network unreachable")

    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "fake_key_for_testing")
    monkeypatch.setattr(requests, "get", raise_connection_error)


def test_fetch_rates_returns_dict(mock_successful_response, monkeypatch):
    """Test that fetch_rates returns a dictionary."""
    monkeypatch.setattr("src.api_client.save_rates", lambda data: None)

    result = fetch_rates()

    assert isinstance(result, dict)


def test_fetch_rates_contains_expected_keys(mock_successful_response, monkeypatch):
    """Test that the returned data contains expected keys."""
    monkeypatch.setattr("src.api_client.save_rates", lambda data: None)

    result = fetch_rates()

    assert "success" in result
    assert "base" in result
    assert "date" in result
    assert "rates" in result


def test_fetch_rates_correct_values(mock_successful_response, monkeypatch):
    """Test that the returned data contains correct values."""
    monkeypatch.setattr("src.api_client.save_rates", lambda data: None)

    result = fetch_rates()

    assert result["success"] is True
    assert result["base"] == "EUR"
    assert result["rates"]["USD"] == 1.18


def test_fetch_rates_calls_save_rates(mock_successful_response, monkeypatch):
    """Test that save_rates is called on successful fetch."""
    saved_data = {}

    def capture_save(data):
        saved_data.update(data)

    monkeypatch.setattr("src.api_client.save_rates", capture_save)

    fetch_rates()

    assert saved_data["base"] == "EUR"
    assert "rates" in saved_data


def test_fetch_rates_no_api_key(monkeypatch):
    """Test that ValueError is raised when API key is missing."""
    monkeypatch.delenv("EXCHANGE_RATE_API_KEY", raising=False)

    with pytest.raises(ValueError, match="EXCHANGE_RATE_API_KEY"):
        fetch_rates()


def test_fetch_rates_api_error(mock_failed_response, monkeypatch):
    """Test that ValueError is raised when API returns unsuccessful response."""
    monkeypatch.setattr("src.api_client.save_rates", lambda data: None)

    with pytest.raises(ValueError, match="API error"):
        fetch_rates()


def test_fetch_rates_network_error(mock_network_error):
    """Test that ConnectionError is raised on network failure."""
    with pytest.raises(requests.exceptions.ConnectionError):
        fetch_rates()


def test_fetch_rates_http_error(monkeypatch):
    """Test that HTTPError is raised on bad status code."""
    class MockResponse:
        """Simulates an HTTP response with a server error status code."""
        status_code = 500

        def raise_for_status(self):
            """Raise an HTTPError to simulate a failed request."""
            raise requests.exceptions.HTTPError("500 Server Error")

    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "fake_key_for_testing")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_rates()
