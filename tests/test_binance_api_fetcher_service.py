"""Test binance_api_fetcher service."""
from unittest import TestCase
from unittest.mock import MagicMock

from binance_api_fetcher.model import Service
import pytest


class TestService(TestCase):
    """Class to unit test the Service class functions.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.

    Attributes:
        service: Service class instance that will be used in every unit test.
        service_args: Args used to create the Service instance.
    """

    # Attributes/Args:
    #     mock_service_source: MagicMock to configure the behaviour of the
    #         Source class.
    #     mock_service_target: MagicMock to configure the behaviour of the
    #         Target class.

    service: Service
    service_args: MagicMock
    # mock_service_source: MagicMock
    # mock_service_target: MagicMock

    # @patch(target="veve_account_validation._service.target.Target")
    # @patch(target="veve_account_validation._service.source.Source")
    def setUp(
        self,
        # mock_service_source: MagicMock,
        # mock_service_target: MagicMock,
    ) -> None:
        """Create a service instance to use in all tests.

        We use the mocks in order to prevent the Service constructor
        to call functions, so we can use and test them, otherwise we
        have ValueErrors because of the packages that should not be
        addressed by these tests.
        """
        # Create the service args with the needed arguments
        self.service_args = MagicMock(
            log_level="debug",
            run_as_service=True,
            dry_run=False,
            source=(
                "user=username password=password "
                "host=localhost port=5432 dbname=binance"
            ),
            target=(
                "user=username password=password "
                "host=localhost port=5432 dbname=binance"
            ),
            min_sleep=0,
            max_sleep=1,
            symbol=True,
            kline_1d=True,
            datapoint_limit=1000,
            shard=1,
        )
        # Create a Service instance for all tests
        self.service = Service(args=self.service_args)
        # # Save the constructor mocks
        # self.mock_service_source = mock_service_source
        # self.mock_service_target = mock_service_target

    @pytest.mark.unit
    def test_service_init_(
        self,
    ) -> None:
        """Test the Service __init__ function.

        Test if:
            1. Attributes of the Service instance have the args
            received assigned;
            2. Attributes of the Service instance have the mocks
            assigned, i.e. the Source and Target mocks;
            3. The calls to the Source and Target constructors are made;
            4. The calls to the functions are made.
        """
        self._test_init_args_assignment()
        # self._test_init_constructor_assignment()
        # self._test_init_constructor_calls()
        # self._test_init_func_calls()

    def _test_init_args_assignment(self) -> None:
        """Test if args are assigned."""
        self.assertEqual(
            first=self.service._run_as_service, second=self.service_args.run_as_service
        )
        self.assertEqual(
            first=self.service._dry_run,
            second=self.service_args.dry_run,
        )
        self.assertEqual(
            first=self.service._source,
            second=self.service_args.source,
        )
        self.assertEqual(
            first=self.service._target,
            second=self.service_args.target,
        )
        self.assertEqual(
            first=self.service._min_sleep, second=self.service_args.min_sleep
        )
        self.assertEqual(
            first=self.service._max_sleep, second=self.service_args.max_sleep
        )
        self.assertEqual(first=self.service._symbol, second=self.service_args.symbol)
        self.assertEqual(
            first=self.service._kline_1d, second=self.service_args.kline_1d
        )
        self.assertEqual(
            first=self.service._datapoint_limit,
            second=self.service_args.datapoint_limit,
        )
        self.assertEqual(first=self.service._shard, second=self.service_args.shard)

    # def _test_init_constructor_assignment(self) -> None:
    #     """Test if the constructors are assigned."""
    #     self.assertEqual(
    #         first=self.service._source, second=self.mock_service_source.return_value
    #     )
    #     self.assertEqual(
    #         first=self.service._target, second=self.mock_service_target.return_value
    #     )
    #     self.assertEqual(
    #         first=self.service._nats_client,
    #         second=self.mock_service_nats_client.return_value,
    #     )

    # def _test_init_constructor_calls(self) -> None:
    #     """Test if the constructors are called."""
    #     self.mock_service_source.assert_called_once_with(self.service_args.source)
    #     self.mock_service_target.assert_called_once_with(self.service_args.target)
    #     self.mock_service_nats_client.assert_called_once()

    # def _test_init_func_calls(self) -> None:
    #     """Test if the function are called."""
    #     self.mock_service_declare_metrics.assert_called_once()
