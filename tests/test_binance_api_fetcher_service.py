"""Test binance_api_fetcher Service class."""

from datetime import UTC
from unittest import TestCase
from unittest.mock import MagicMock, patch

from binance_api_fetcher.service import Service  # type: ignore
import pytest


class TestService(TestCase):
    """Class to test the Service class functions.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.

    Attributes:
        service: Service class instance that will be used in every unit test.
        service_args: Args used to create the Service instance.
        mock_service_source_component: MagicMock to configure the behaviour
            of the Source class.
        mock_service_target_component: MagicMock to configure the behaviour
            of the Target class.
    """

    service: Service
    service_args: MagicMock
    mock_service_source: MagicMock
    mock_service_target: MagicMock

    @patch(target="binance_api_fetcher.service.Target")
    @patch(target="binance_api_fetcher.service.Source")
    def setUp(
        self,
        mock_service_source: MagicMock,
        mock_service_target: MagicMock,
    ) -> None:
        """Create a service instance to use in all tests.

        We use the mocks in order to prevent the Service constructor
        to call functions, so we can use and test them, otherwise we
        have ValueErrors because of the packages that should not be
        addressed by these tests.

        Args:
            mock_service_source: MagicMock to configure the behaviour
                of the Source class.
            mock_service_target: MagicMock to configure the behaviour
                of the Target class.
        """
        # Save the constructor mocks
        self.mock_service_source = mock_service_source
        self.mock_service_target = mock_service_target

        # Set up the service args with the needed arguments
        self.service_args = MagicMock(
            log_level="debug",
            run_as_service=True,
            dry_run=False,
            source_info=(
                "user=username password=password "
                "host=localhost port=5432 dbname=binance"
            ),
            target_info=(
                "user=username password=password "
                "host=localhost port=5432 dbname=binance"
            ),
            min_sleep=0,
            max_sleep=1,
            source_ping="ping",
            source_request_timeout=120,
            symbol="ethbtc",
            kline_1d=True,
            datapoint_limit=1000,
        )
        # Set up a Service instance for all tests (call the __init__ function)
        self.service = Service(args=self.service_args)

        # TODO Set up service._entities???

    def test_init_args_assignment(self) -> None:
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
            first=self.service._source_info,
            second=self.service_args.source_info,
        )
        self.assertIsInstance(obj=self.service._source_info, cls=str)
        # target
        self.assertEqual(
            first=self.service._target_info,
            second=self.service_args.target_info,
        )
        self.assertIsInstance(obj=self.service._target_info, cls=str)
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
        # source_ping
        self.assertEqual(
            first=self.service._source_ping,
            second=self.service_args.source_ping,
        )
        self.assertIsInstance(obj=self.service._source_ping, cls=str)
        # source_request_timeout
        self.assertEqual(
            first=self.service._source_request_timeout,
            second=self.service_args.source_request_timeout,
        )
        self.assertIsInstance(obj=self.service._source_request_timeout, cls=int)
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

    def test_init_constructor_call_and_assignment(self) -> None:
        """Test if constructors are called and assigned.

        Test if constructors are called and assigned in the __init__ function,
        by comparing the service source and target components with the
        Source and Target constructors calls and return values.
        """
        # Assert constructor calls
        self.mock_service_source.assert_called_once_with(
            connection_string=self.service._source_info,
            ping_string=self.service._source_ping,
            request_timeout=self.service._source_request_timeout,
        )
        self.mock_service_target.assert_called_once_with(
            connection_string=self.service._target_info
        )
        # Assert constructor assignments
        self.assertEqual(
            first=self.service._source,
            second=self.mock_service_source.return_value,
        )
        self.assertEqual(
            first=self.service._target,
            second=self.mock_service_target.return_value,
        )

    @patch.object(target=Service, attribute="tear_down")
    @patch(target="binance_api_fetcher.service.logger.info")
    @patch.object(target=Service, attribute="run_once")
    @patch.object(target=Service, attribute="run_service")
    @pytest.mark.unit
    def test_service_run_with_run_as_service(
        self,
        mock_run_service: MagicMock,
        mock_run_once: MagicMock,
        mock_logger_info: MagicMock,
        mock_tear_down: MagicMock,
    ) -> None:
        """Test the Service run function.

        Test if:
            1. Source and Target components call their connect method;
            2. The call to the run_service function is made;
            3. The call to the run_once function is not made;
            4. The call to the tear_down function is made.

        Args:
            mock_run_service: Mock for run_service function call.
            mock_run_once: Mock for run_once function call.
            mock_logger_info: Mock for logger.info function call.
            mock_tear_down: Mock for tear_down function call.
        """
        # Save orignal value of run_as_service
        attr_original_value: bool = self.service._run_as_service
        # Change orignal value of run_as_service
        self.service._run_as_service = True

        # Call the run function
        self.service.run()

        # Assert Source and Target connect function calls
        self.mock_service_source.return_value.connect.assert_called_once()
        self.mock_service_target.return_value.connect.assert_called_once()
        # Assert logger.info is called with the correct message
        mock_logger_info.assert_called_once_with(msg="Running the service continuosly.")
        # Assert run_service is called exactly once
        mock_run_service.assert_called_once()
        # Assert run once is not called
        mock_run_once.assert_not_called()
        # Assert tear_down is called exactly once
        mock_tear_down.assert_called_once()

        # Reset orignal value of run_as_service
        self.service._run_as_service = attr_original_value

    @patch.object(target=Service, attribute="tear_down")
    @patch(target="binance_api_fetcher.service.logger.info")
    @patch.object(target=Service, attribute="run_once")
    @patch.object(target=Service, attribute="run_service")
    @pytest.mark.unit
    def test_service_run_without_run_as_service(
        self,
        mock_run_service: MagicMock,
        mock_run_once: MagicMock,
        mock_logger_info: MagicMock,
        mock_tear_down: MagicMock,
    ) -> None:
        """Test the Service run function.

        Test if:
            1. Source and Target components call their connect method;
            2. The call to the run_service function is made;
            3. The call to the run_once function is not made;
            4. The call to the tear_down function is made.

        Args:
            mock_run_service: Mock for run_service function call.
            mock_run_once: Mock for run_once function call.
            mock_logger_info: Mock for logger.info function call.
            mock_tear_down: Mock for tear_down function call.
        """
        # Save orignal value of run_as_service
        attr_original_value: bool = self.service._run_as_service
        # Change orignal value of run_as_service
        self.service._run_as_service = False

        # Call the run function
        self.service.run()

        # Assert Source and Target connect function calls
        self.mock_service_source.return_value.connect.assert_called_once()
        self.mock_service_target.return_value.connect.assert_called_once()

        # Assert logger.info is called with the correct message
        mock_logger_info.assert_called_once_with(msg="Running the service once.")
        # Assert run_service is not called
        mock_run_service.assert_not_called()
        # Assert run once is called exactly once
        mock_run_once.assert_called_once()
        # Assert tear_down is called exactly once
        mock_tear_down.assert_called_once()

        # Reset orignal value of run_as_service
        self.service._run_as_service = attr_original_value

    @patch(target="binance_api_fetcher.service.logger")
    @patch.object(
        target=Service, attribute="run_once", side_effect=Exception("Testing error")
    )
    @pytest.mark.unit
    def test_service_run_service(
        self,
        mock_run_once: MagicMock,
        mock_logger: MagicMock,
    ) -> None:
        """Test the Service run_service function.

        Test if:
            1. The call to the run_once function is made;
            2. The call to the random_sleep function is made;
            3. The Exception is catched and a message is logged.

        Args:
            mock_run_once: Mock for run_once function call.
            mock_logger: Mock for logger.info and logger.error function calls.
        """
        # Call the run_service function
        self.service.run_service()

        # Assert run_once is called exactly once
        mock_run_once.assert_called_once()
        # Assert logger.error is called with the correct message
        mock_logger.error.assert_called_once_with(
            msg="Error running service: " "Exception - Testing error."
        )
        # Assert logger.info is called with the correct message
        mock_logger.info.assert_called_once_with(msg="Terminating continuous run.")

    @patch(target="binance_api_fetcher.service.logger")
    @patch(target="binance_api_fetcher.service.Target")
    @patch(target="binance_api_fetcher.service.Entity")
    @patch(target="binance_api_fetcher.service.secrets.choice")
    @patch(target="binance_api_fetcher.service.datetime")
    @pytest.mark.unit
    def test_service_run_once_success(
        self,
        mock_datetime: MagicMock,
        mock_secrets_choice: MagicMock,
        mock_entity: MagicMock,
        mock_target: MagicMock,
        mock_logger: MagicMock,
    ) -> None:
        """Test the Service run_once function.

        Test if:
            1. asdasdasd;
            2. asdasd.

        Args:
            mock_datetime: mock for the datetime function calls.
            mock_secrets_choice: Mock for secrets choice function call.
            mock_entity: Mock for Entity class.
            mock_target: Mock for Target function calls.
            mock_logger: Mock for logger function calls.
        """
        # Set up new target value
        old_attr = self.service._target
        self.service._target = mock_target
        # Set up mock return values
        mock_datetime.now.return_value = mock_datetime
        mock_secrets_choice.return_value = mock_entity
        mock_target.get_next_delivery_id.return_value = 1
        #  Set up test variables
        test_start_and_end_time = mock_datetime.now.return_value
        test_entity = mock_secrets_choice.return_value
        test_delivery_id = mock_target.get_next_delivery_id.return_value

        # Call run_once
        self.service.run_once()

        # Assert that datetime.now is called with the correct arguments
        mock_datetime.now.assert_called_with(tz=UTC)
        assert mock_datetime.now.call_count == 2
        # Assert that secrets.choice  is called with the correct arguments
        mock_secrets_choice.assert_called_once_with(seq=list(self.service._entities))
        # Assert that logger.info is called with the correct message
        mock_logger.info.assert_called_once_with(
            msg=f"Delivery {test_delivery_id} (Entity {test_entity}): processed "
            f"({test_start_and_end_time - test_start_and_end_time} "
            "seconds)."
        )

        # Tear down - reset target value
        self.service._target = old_attr

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
            1. Source and Target components call their disconnect method.
        """
        # Call the run function
        self.service.tear_down()

        # Assert Source and Target connect function calls
        self.mock_service_source.return_value.disconnect.assert_called_once()
        self.mock_service_target.return_value.disconnect.assert_called_once()
