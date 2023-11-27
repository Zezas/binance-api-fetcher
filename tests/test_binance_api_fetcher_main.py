"""Test binance_api_fetcher __main__."""
from argparse import Namespace
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

from pytest import MonkeyPatch

from binance_api_fetcher.__main__ import main, parse_args


class TestMain(TestCase):
    """Class to unit test the __main__ file functions.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.
    """

    @patch.object(target=sys, attribute="argv", new=[])
    def test_parse_args_default(self) -> None:
        """Test the parse_args function with default values.

        In this test we empty the argv and assert the default
        values returned by the parse_args_functions.
        """
        # Execute the parse_args function
        args = parse_args()

        # Test for default values
        self.assertIsInstance(obj=args, cls=Namespace)
        self.assertTrue(expr=args.run_as_service)
        self.assertFalse(expr=args.dry_run)
        self.assertIsNone(obj=args.source)
        self.assertIsNone(obj=args.target)
        self.assertEqual(first=args.min_sleep, second=15)
        self.assertEqual(first=args.max_sleep, second=30)
        self.assertFalse(expr=args.symbol)
        self.assertFalse(expr=args.kline_1d)
        self.assertEqual(first=args.datapoint_limit, second=500)
        self.assertEqual(first=args.shard, second=0)

    @patch.object(target=sys, attribute="argv", new=[])
    def test_parse_args_not_default(self) -> None:
        """Test the parse_args function with non default values.

        In this test we empty the argv and then set all env variables
        before asserting the values returned by the parse_args_function.
        """
        # TODO refactor into smaller functions
        # Create a monkeypatch obj
        monkeypatch: MonkeyPatch = MonkeyPatch()
        # Set environment
        monkeypatch.setenv(name="RUN_AS_SERVICE", value="False")
        monkeypatch.setenv(name="DRY_RUN", value="True")
        monkeypatch.setenv(name="SOURCE", value="source")
        monkeypatch.setenv(name="TARGET", value="target")
        monkeypatch.setenv(name="MIN_SLEEP", value="0")
        monkeypatch.setenv(name="MAX_SLEEP", value="1")
        monkeypatch.setenv(name="SYMBOL", value="True")
        monkeypatch.setenv(name="KLINE_1D", value="True")
        monkeypatch.setenv(name="DATAPOINT_LIMIT", value="1000")
        monkeypatch.setenv(name="SHARD", value="1")

        # Execute the parse_args function
        args = parse_args()

        # Test for non default values
        self.assertIsInstance(obj=args, cls=Namespace)
        self.assertFalse(expr=args.run_as_service)
        self.assertTrue(expr=args.dry_run)
        self.assertIsNotNone(obj=args.source)
        self.assertEqual(first=args.source, second="source")
        self.assertIsNotNone(obj=args.target)
        self.assertEqual(first=args.target, second="target")
        self.assertEqual(first=args.min_sleep, second=0)
        self.assertEqual(first=args.max_sleep, second=1)
        self.assertTrue(expr=args.symbol)
        self.assertTrue(expr=args.kline_1d)
        self.assertEqual(first=args.datapoint_limit, second=1000)
        self.assertEqual(first=args.shard, second=1)

    @patch(target="binance_api_fetcher.__main__.logger")
    @patch(target="binance_api_fetcher.__main__.parse_args")
    def test_main_run(
        self,
        mock_parse_args: MagicMock,
        mock_logger: MagicMock,
    ) -> None:
        """Test the execution of the main function.

        In this test we create mocks for every statement called in
        the main function and assert if they are called once with the
        right attributes.

        Args:
            mock_parse_args: Mock for parse_args().
            mock_logger: Mock for logger.info().
        """
        # run it
        main()

        # Assert that each function is called once
        mock_logger.info.assert_called_once_with("Starting service...")
        mock_parse_args.assert_called_once()
