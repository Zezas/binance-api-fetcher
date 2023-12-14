"""Test binance_api_fetcher Target class."""

from unittest import TestCase

from binance_api_fetcher.persistence import Target
import pytest


class TestTarget(TestCase):
    """Class to test the Target class functions.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.

    Attributes:
        target: Target class instance that will be used in every unit test.
        test_connection_string: String used to create the Target instance.
    """

    target: Target
    test_connection_string: str

    def setUp(self) -> None:
        """Create a target instance to use in all tests.

        We use the mocks in order to prevent the Target constructor
        to call functions, so we can use and test them, otherwise we
        have ValueErrors because of the packages that should not be
        addressed by these tests.
        """
        # Create a connection string used by the target
        self.test_connection_string: str = (
            "user=username password=password " "host=localhost port=5432 dbname=binance"
        )
        # Set up a Target instance for all tests (call the __init__ function)
        self.target = Target(connection_string=self.test_connection_string)

    @pytest.mark.unit
    def test_target_init(
        self,
    ) -> None:
        """Test the Target __init__ function.

        Test if:
            1. Attributes of the Target instance have the args
            received and default values assigned.
        """
        # connection_string
        self.assertEqual(
            first=self.target._connection_string,
            second=self.test_connection_string,
        )
        self.assertIsInstance(obj=self.target._connection_string, cls=str)
        # transaction_in_progress
        self.assertEqual(
            first=self.target._transaction_in_progress,
            second=False,
        )
        self.assertIsInstance(obj=self.target._transaction_in_progress, cls=bool)
