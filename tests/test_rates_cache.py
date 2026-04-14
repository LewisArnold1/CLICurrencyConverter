# pylint: disable=redefined-outer-name
"""Tests for the rates cache module."""

import json
import pytest

from src.rates_cache import load_rates


@pytest.fixture
def sample_rates_data():
    """Provide sample exchange rate data for testing."""
    return {
        "success": True,
        "base": "EUR",
        "date": "2026-04-14",
        "rates": {"USD": 1.18, "GBP": 0.87},
    }


@pytest.fixture
def sample_rates_file(tmp_path, sample_rates_data):
    """Create a temporary rates file with sample data."""
    file_path = tmp_path / "test_rates.json"
    file_path.write_text(json.dumps(sample_rates_data))
    return str(file_path)


def test_load_rates_returns_dict(sample_rates_file):
    """Test that load_rates returns a dictionary."""
    result = load_rates(sample_rates_file)

    assert isinstance(result, dict)


def test_load_rates_contains_expected_keys(sample_rates_file):
    """Test that the returned data contains the expected keys."""
    result = load_rates(sample_rates_file)

    assert "success" in result
    assert "base" in result
    assert "date" in result
    assert "rates" in result


def test_load_rates_correct_values(sample_rates_file):
    """Test that the returned data matches the file contents."""
    result = load_rates(sample_rates_file)

    assert result["base"] == "EUR"
    assert result["rates"]["USD"] == 1.18
    assert result["rates"]["GBP"] == 0.87


def test_load_rates_file_not_found():
    """Test that FileNotFoundError is raised for a missing file."""
    with pytest.raises(FileNotFoundError):
        load_rates("nonexistent_file.json")


def test_load_rates_invalid_json(tmp_path):
    """Test that JSONDecodeError is raised for invalid JSON."""
    file_path = tmp_path / "bad_rates.json"
    file_path.write_text("this is not valid json")

    with pytest.raises(json.JSONDecodeError):
        load_rates(str(file_path))


def test_load_rates_empty_file(tmp_path):
    """Test that JSONDecodeError is raised for an empty file."""
    file_path = tmp_path / "empty.json"
    file_path.write_text("")

    with pytest.raises(json.JSONDecodeError):
        load_rates(str(file_path))


def test_load_rates_default_file():
    """Test that the default last_rates.json file loads successfully."""
    result = load_rates()

    assert result["success"] is True
    assert result["base"] == "EUR"
    assert len(result["rates"]) > 0
