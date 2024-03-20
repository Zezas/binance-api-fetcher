"""Test binance_api_fetcher package version."""

from unittest import TestCase

from binance_api_fetcher import __version__  # type: ignore
import pytest


class TestVersion(TestCase):
    """Class to test the package version.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.
    """

    @pytest.mark.unit
    def test_version(self) -> None:
        """Test binance_api_fetcher package version.

        Test if the binance_api_fetcher __version__ is the same
        as the one presented in the pyproject.toml file
        """
        self.assertEqual(first=__version__, second="0.1.0")
