# pylint: disable=redefined-outer-name
"""Tests for the rates cache module."""

import json
import os
import pytest


from src.rates_cache import load_rates, save_rates


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


@pytest.fixture
def saved_rates_file(tmp_path, sample_rates_data):
    """Save sample data to a temporary file and return the path."""
    file_path = str(tmp_path / "rates.json")
    save_rates(sample_rates_data, file_path)
    return file_path


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


def test_save_rates_creates_file(saved_rates_file):
    """Test that save_rates creates a new file."""
    assert os.path.exists(saved_rates_file)


def test_save_rates_content_matches(saved_rates_file, sample_rates_data):
    """Test that the saved file contains the correct data."""
    with open(saved_rates_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == sample_rates_data


def test_save_rates_overwrites_existing(saved_rates_file):
    """Test that save_rates overwrites an existing file."""
    # Arrange
    new_data = {"success": True, "base": "EUR", "date": "2099-01-01", "rates": {"USD": 2.0}}

    # Act
    save_rates(new_data, saved_rates_file)

    # Assert
    with open(saved_rates_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data["date"] == "2099-01-01"


def test_save_and_load_roundtrip(saved_rates_file, sample_rates_data):
    """Test that data survives a save then load cycle."""
    result = load_rates(saved_rates_file)
    assert result == sample_rates_data
