"""Test binance_api_fetcher Service class."""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from binance_api_fetcher.model import Service
import pytest


class TestService(TestCase):
    """Class to test the Service class functions.

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
        # Set up the service args with the needed arguments
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
            symbol="ethbtc",
            kline_1d=True,
            datapoint_limit=1000,
            shard=1,
        )
        # Set up a Service instance for all tests
        self.service = Service(args=self.service_args)
        # # Save the constructor mocks
        # self.mock_service_source = mock_service_source
        # self.mock_service_target = mock_service_target

    @pytest.mark.unit
    def test_service_init(
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
        """Test if args are assigned.

        Test if args are assigned in the __init__ function,
        by comparing the service and args attributes and checking
        the types of the attributes.
        """
        # run_as_service
        self.assertEqual(
            first=self.service._run_as_service, second=self.service_args.run_as_service
        )
        self.assertIsInstance(obj=self.service._run_as_service, cls=bool)
        # dry_run
        self.assertEqual(
            first=self.service._dry_run,
            second=self.service_args.dry_run,
        )
        self.assertIsInstance(obj=self.service._dry_run, cls=bool)
        # source
        self.assertEqual(
            first=self.service._source,
            second=self.service_args.source,
        )
        self.assertIsInstance(obj=self.service._source, cls=str)
        # target
        self.assertEqual(
            first=self.service._target,
            second=self.service_args.target,
        )
        self.assertIsInstance(obj=self.service._target, cls=str)
        # min_sleep
        self.assertEqual(
            first=self.service._min_sleep, second=self.service_args.min_sleep
        )
        self.assertIsInstance(obj=self.service._min_sleep, cls=int)
        # max_sleep
        self.assertEqual(
            first=self.service._max_sleep, second=self.service_args.max_sleep
        )
        self.assertIsInstance(obj=self.service._max_sleep, cls=int)
        # symbol
        self.assertEqual(first=self.service._symbol, second=self.service_args.symbol)
        self.assertIsInstance(obj=self.service._symbol, cls=str)
        # kline_1d
        self.assertEqual(
            first=self.service._kline_1d, second=self.service_args.kline_1d
        )
        self.assertIsInstance(obj=self.service._kline_1d, cls=bool)
        # datapoint_limit
        self.assertEqual(
            first=self.service._datapoint_limit,
            second=self.service_args.datapoint_limit,
        )
        self.assertIsInstance(obj=self.service._datapoint_limit, cls=int)
        # shard
        self.assertEqual(first=self.service._shard, second=self.service_args.shard)
        self.assertIsInstance(obj=self.service._shard, cls=int)

    # def _test_init_constructor_assignment(self) -> None:
    #     """Test if constructors are assigned.
    #
    #     Test if constructors are assigned in the __init__ function,
    #     by comparing the service source and target attributes with the
    #     Source and Target constructors return value.
    #     """
    #     self.assertEqual(
    #         first=self.service._source, second=self.mock_service_source.return_value
    #     )
    #     self.assertEqual(
    #         first=self.service._target, second=self.mock_service_target.return_value
    #     )

    # def _test_init_constructor_calls(self) -> None:
    #     """Test if constructors are called.
    #
    #     Test if constructors are called in the __init__ function,
    #     with the respective arguments.
    #     """
    #     self.mock_service_source.assert_called_once_with(self.service_args.source)
    #     self.mock_service_target.assert_called_once_with(self.service_args.target)
    #     self.mock_service_nats_client.assert_called_once()

    # def _test_init_func_calls(self) -> None:
    #     """Test if functions are called.
    #
    #     Test if functions are called in the __init__ function,
    #     with the respective arguments.
    #     """
    #     self.mock_service_declare_metrics.assert_called_once()

    @pytest.mark.unit
    def test_service_run(
        self,
    ) -> None:
        """Test the Service run function.

        Test if:
            1. Source and Target components call their connect method;
            2. The call to the run_service function is made;
            3. The call to the run_once function is made;
            4. The call to the tear_down function is made.

        These tests are made by testing each scenario of the run function,
        i.e. with the _run_as_service attribute set to True and False.
        """
        self._test_service_run_with_run_as_service()
        self._test_service_run_without_run_as_service()

    @patch(target="binance_api_fetcher.model.service.Service.run_service")
    def _test_service_run_with_run_as_service(
        self,
        mock_run_service: MagicMock,
    ) -> None:
        """Test the Service run function with run_as_service.

        Test if:
            1. Source and Target components call their connect method;
            2. The call to the run_service function is made;
            3. The call to the tear_down function is made.

        Args:
            mock_run_service: Mock for run_service function call.
        """
        # Save orignal value of run_as_service
        attr_original_value: bool = self.service._run_as_service
        # Change orignal value of run_as_service
        self.service._run_as_service = True

        # Call function to test
        self.service.run()

        #  Test if calls are made
        mock_run_service.assert_called_once()

        # Reset orignal value of run_as_service
        self.service._run_as_service = attr_original_value

    @patch(target="binance_api_fetcher.model.service.Service.run_once")
    def _test_service_run_without_run_as_service(
        self,
        mock_run_once: MagicMock,
    ) -> None:
        """Test the Service run function without run_as_service.

        Test if:
            1. Source and Target components call their connect method;
            2. The call to the run_once function is made;
            3. The call to the tear_down function is made.

        Args:
            mock_run_once: Mock for run_once function call.
        """
        # Save orignal value of run_as_service
        attr_original_value: bool = self.service._run_as_service
        # Change orignal value of run_as_service
        self.service._run_as_service = False

        # Call function to test
        self.service.run()

        #  Test if calls are made
        mock_run_once.assert_called_once()

        # Reset orignal value of run_as_service
        self.service._run_as_service = attr_original_value

    @pytest.mark.unit
    def test_service_run_service(
        self,
    ) -> None:
        """Test the Service run_service function.

        Test if:
            1. asdasdasd;
            2. asdasd.
        """
        # TODO implement
        pass

    @pytest.mark.unit
    def test_service_run_once(
        self,
    ) -> None:
        """Test the Service run_once function.

        Test if:
            1. asdasdasd;
            2. asdasd.
        """
        # TODO implement
        pass

    @pytest.mark.unit
    def test_service_scrape(
        self,
    ) -> None:
        """Test the Service scrape function.

        Test if:
            1. asdasdasd;
            2. asdasd.
        """
        # TODO implement
        pass

    @pytest.mark.unit
    def test_service_parse(
        self,
    ) -> None:
        """Test the Service parse function.

        Test if:
            1. asdasdasd;
            2. asdasd.
        """
        # TODO implement
        pass

    @pytest.mark.unit
    def test_service_process(
        self,
    ) -> None:
        """Test the Service process function.

        Test if:
            1. asdasdasd;
            2. asdasd.
        """
        # TODO implement
        pass

    @pytest.mark.unit
    def test_service_compute_events(
        self,
    ) -> None:
        """Test the Service compute_events function.

        Test if:
            1. asdasdasd;
            2. asdasd.
        """
        # TODO implement
        pass

    @pytest.mark.unit
    def test_service_persist_delivery(
        self,
    ) -> None:
        """Test the Service persist_delivery function.

        Test if:
            1. asdasdasd;
            2. asdasd.
        """
        # TODO implement
        pass

    @pytest.mark.unit
    def test_service_persist_to_database(
        self,
    ) -> None:
        """Test the Service persist_to_database function.

        Test if:
            1. asdasdasd;
            2. asdasd.
        """
        # TODO implement
        pass

    @pytest.mark.unit
    def test_service_tear_down(
        self,
    ) -> None:
        """Test the Service tear_down function.

        Test if:
            1. asdasdasd;
            2. asdasd.
        """
        # TODO implement
        pass
