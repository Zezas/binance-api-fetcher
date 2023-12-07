"""Test binance_api_fetcher package version."""

from unittest import TestCase

from binance_api_fetcher import __version__
import pytest


class TestVersion(TestCase):
    """Class to test the package version.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.
    """

    @pytest.mark.unit
    def test_version(self) -> None:
        """Test binance_api_fetcher package version."""
        self.assertEqual(first=__version__, second="0.1.0")
