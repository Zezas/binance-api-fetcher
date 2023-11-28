"""Test binance_api_fetcher package version."""

from binance_api_fetcher import __version__
import pytest


@pytest.mark.unit
def test_version() -> None:
    """Test binance_api_fetcher version."""
    assert __version__ == "0.1.0"
