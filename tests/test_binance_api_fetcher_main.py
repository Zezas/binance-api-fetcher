"""Test binance_api_fetcher __main__ file."""

from argparse import Namespace
import sys
from sys import stdout
from typing import Sequence
from unittest import TestCase
from unittest.mock import call, MagicMock, patch

from binance_api_fetcher.__main__ import logging_config, main, parse_args
import pytest
from pytest import MonkeyPatch

TESTING_VERSION: str = "0.0.0"


class TestMain(TestCase):
    """Class to test the __main__ file functions.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.
    """

    @patch.object(target=sys, attribute="argv", new=[])
    @pytest.mark.unit
    def test_parse_args_default(self) -> None:
        """Test the parse_args function with default values.

        In this test we empty the argv and assert the default
        values and types returned by the parse_args_functions.
        """
        # Execute the parse_args function
        args = parse_args()

        # Test args for default values
        self.assertIsInstance(obj=args, cls=Namespace)
        # log_level
        self.assertEqual(first=args.log_level, second="info")
        self.assertIsInstance(obj=args.log_level, cls=str)
        # run_as_service
        self.assertTrue(expr=args.run_as_service)
        self.assertIsInstance(obj=args.run_as_service, cls=bool)
        # dry_run
        self.assertFalse(expr=args.dry_run)
        self.assertIsInstance(obj=args.dry_run, cls=bool)
        # source
        self.assertEqual(first=args.source, second="")
        self.assertIsInstance(obj=args.source, cls=str)
        # target
        self.assertEqual(first=args.target, second="")
        self.assertIsInstance(obj=args.target, cls=str)
        # min_sleep
        self.assertEqual(first=args.min_sleep, second=15)
        self.assertIsInstance(obj=args.min_sleep, cls=int)
        # max_sleep
        self.assertEqual(first=args.max_sleep, second=30)
        self.assertIsInstance(obj=args.max_sleep, cls=int)
        # symbol
        self.assertEqual(first=args.symbol, second="")
        self.assertIsInstance(obj=args.symbol, cls=str)
        # kline_1d
        self.assertFalse(expr=args.kline_1d)
        self.assertIsInstance(obj=args.kline_1d, cls=bool)
        # datapoint_limit
        self.assertEqual(first=args.datapoint_limit, second=500)
        self.assertIsInstance(obj=args.datapoint_limit, cls=int)
        # shard
        self.assertEqual(first=args.shard, second=0)
        self.assertIsInstance(obj=args.shard, cls=int)

    @patch.object(target=sys, attribute="argv", new=[])
    @pytest.mark.unit
    def test_parse_args_not_default(self) -> None:
        """Test the parse_args function with non default values.

        In this test we empty the argv and then set all env variables
        before asserting the values and types returned by the
        parse_args_function.
        """
        # Set up a monkeypatch obj
        monkeypatch: MonkeyPatch = MonkeyPatch()
        # Set up environment variables
        monkeypatch.setenv(name="LOG_LEVEL", value="debug")
        monkeypatch.setenv(name="RUN_AS_SERVICE", value="False")
        monkeypatch.setenv(name="DRY_RUN", value="True")
        monkeypatch.setenv(name="SOURCE", value="source")
        monkeypatch.setenv(name="TARGET", value="target")
        monkeypatch.setenv(name="MIN_SLEEP", value="0")
        monkeypatch.setenv(name="MAX_SLEEP", value="1")
        monkeypatch.setenv(name="SYMBOL", value="ethbtc")
        monkeypatch.setenv(name="KLINE_1D", value="True")
        monkeypatch.setenv(name="DATAPOINT_LIMIT", value="1000")
        monkeypatch.setenv(name="SHARD", value="1")

        # Execute the parse_args function
        args = parse_args()

        # Assert args for non default values
        self.assertIsInstance(obj=args, cls=Namespace)
        # log_level
        self.assertEqual(first=args.log_level, second="debug")
        self.assertIsInstance(obj=args.log_level, cls=str)
        # run_as_service
        self.assertFalse(expr=args.run_as_service)
        self.assertIsInstance(obj=args.run_as_service, cls=bool)
        # dry_run
        self.assertTrue(expr=args.dry_run)
        self.assertIsInstance(obj=args.dry_run, cls=bool)
        # source
        self.assertEqual(first=args.source, second="source")
        self.assertIsInstance(obj=args.source, cls=str)
        # target
        self.assertEqual(first=args.target, second="target")
        self.assertIsInstance(obj=args.target, cls=str)
        # min_sleep
        self.assertEqual(first=args.min_sleep, second=0)
        self.assertIsInstance(obj=args.min_sleep, cls=int)
        # max_sleep
        self.assertEqual(first=args.max_sleep, second=1)
        self.assertIsInstance(obj=args.max_sleep, cls=int)
        # symbol
        self.assertEqual(first=args.symbol, second="ethbtc")
        self.assertIsInstance(obj=args.symbol, cls=str)
        # kline_1d
        self.assertTrue(expr=args.kline_1d)
        self.assertIsInstance(obj=args.kline_1d, cls=bool)
        # datapoint_limit
        self.assertEqual(first=args.datapoint_limit, second=1000)
        self.assertIsInstance(obj=args.datapoint_limit, cls=int)
        # shard
        self.assertEqual(first=args.shard, second=1)
        self.assertIsInstance(obj=args.shard, cls=int)

    @patch(target="binance_api_fetcher.__main__.logging")
    @pytest.mark.unit
    def test_logging_config(
        self,
        mock_logging: MagicMock,
    ) -> None:
        """Test the logging_config function execution.

        In this test we check if the logging_config function
        is executed with the right parameters, i.e. if it calls
        the logging.basicConfig with the expected configuration.

        Args:
            mock_logging: Mock for logging.basicConfig().
        """
        # Set up logging_level
        logging_level: str = "debug"

        # Execute the logging_level function
        logging_config(logging_level=logging_level)

        # Test logging.basicConfig is called once with the correct arguments
        mock_logging.basicConfig.assert_called_once_with(
            level=logging_level.upper(),
            format=(
                "%(asctime)s.%(msecs)06d %(levelname)s "
                "[%(filename)s:%(lineno)d] %(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
            stream=stdout,
        )

    @patch(target="binance_api_fetcher.__main__.__version__", new=TESTING_VERSION)
    @patch(target="binance_api_fetcher.__main__.parse_args")
    @patch(target="binance_api_fetcher.__main__.logging_config")
    @patch(target="binance_api_fetcher.__main__.logger")
    @patch(target="binance_api_fetcher.__main__.Service")
    @pytest.mark.unit
    def test_main_run(
        self,
        mock_service: MagicMock,
        mock_logger: MagicMock,
        mock_logging_config: MagicMock,
        mock_parse_args: MagicMock,
    ) -> None:
        """Test the execution of the main function.

        In this test we create mocks for every statement called in
        the main function and assert if they are called with the
        right attributes.

        Args:
            mock_service: Mock for Service class call.
            mock_logger: Mock for logger.info().
            mock_logging_config: Mock for logging_config().
            mock_parse_args: Mock for parse_args().
        """
        # Set up the expected calls for the logger.info
        logger_info_expected_calls: Sequence = [
            call(
                msg=(
                    "Starting binance-delivery-fetcher " f"v{TESTING_VERSION} service."
                )
            ),
            call(
                msg=(
                    "Service binance-delivery-fetcher " f"v{TESTING_VERSION} shutdown."
                )
            ),
        ]

        # Execute the main function
        main()

        # Assert parse_args is called once
        mock_parse_args.assert_called_once()
        # Assert logging_config is called once with the correct arguments
        mock_logging_config.assert_called_once_with(
            logging_level=mock_parse_args.return_value.log_level
        )

        # Assert logger.info has the expected calls in the right order
        mock_logger.info.assert_has_calls(logger_info_expected_calls, any_order=False)
        # Assert logger.info has the expected number of calls
        self.assertEqual(first=mock_logger.info.call_count, second=2)

        # Assert service constructor is called once with the correct arguments
        mock_service.assert_called_once_with(args=mock_parse_args.return_value)
        # Assert service.run is called once with the correct arguments
        mock_service.return_value.run.assert_called_once()
