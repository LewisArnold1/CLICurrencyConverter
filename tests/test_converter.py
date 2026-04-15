# pylint: disable=redefined-outer-name
"""Tests for the converter module."""

import pytest

from src.converter import convert_currency


@pytest.fixture
def sample_rates():
    """Sample exchange rates with EUR as base."""
    return {
        "USD": 1.18,
        "GBP": 0.87,
        "JPY": 130.0,
    }


@pytest.mark.parametrize(
    "base, target, amount, expected",
    [
        pytest.param("EUR", "USD", 100, 118.0, id="EUR to USD"),
        pytest.param("USD", "EUR", 118, 100.0, id="USD to EUR"),
        pytest.param("USD", "GBP", 118, 87.0, id="USD to GBP via EUR"),
        pytest.param("USD", "USD", 50, 50.0, id="same currency"),
        pytest.param("EUR", "USD", 0, 0.0, id="zero amount"),
        pytest.param("EUR", "USD", -100, -118.0, id="negative amount"),
        pytest.param("eur", "usd", 100, 118.0, id="case insensitive"),
        pytest.param("EUR", "JPY", 1000000, 130000000.0, id="large amount"),
    ],
)
def test_convert_currency(sample_rates, base, target, amount, expected):
    """Test currency conversion with various inputs."""
    result = convert_currency(base, target, amount, sample_rates)

    assert result == expected


@pytest.mark.parametrize(
    "base, target",
    [
        pytest.param("XYZ", "USD", id="unsupported base"),
        pytest.param("USD", "XYZ", id="unsupported target"),
    ],
)
def test_convert_unsupported_currency(sample_rates, base, target):
    """Test that ValueError is raised for unsupported currencies."""
    with pytest.raises(ValueError, match="Unsupported currency"):
        convert_currency(base, target, 100, sample_rates)


def test_convert_rounds_to_two_decimals(sample_rates):
    """Test that the result is rounded to 2 decimal places."""
    result = convert_currency("JPY", "GBP", 1000, sample_rates)

    assert result == round(1000 / 130.0 * 0.87, 2)
