"""Test binance_api_fetcher Entity class."""

from unittest import TestCase

from binance_api_fetcher.model import Entity  # type: ignore
import pytest


class TestEntity(TestCase):
    """Class to test the Entity enum class.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.
    """

    @pytest.mark.unit
    def test_entity_members_and_values(self) -> None:
        """Test Entity members and values.

        Test if all members of the Entity class exist and have the
        expected values.
        """
        self.assertTrue(Entity.KLINE_1D in Entity)
        self.assertEqual(Entity.KLINE_1D.value, "kline_1d")

    @pytest.mark.unit
    def test_enum_repr(self) -> None:
        """Test the Entity __repr__ function.

        Test if the function call has the expected value for all
        members of the Entity class.
        """
        self.assertEqual(repr(Entity.KLINE_1D), "kline_1d")
