"""Test binance_api_fetcher Target class."""

from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from binance_api_fetcher.persistence import Target, TargetError  # type: ignore
import psycopg2
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
        # is_connected
        self.assertFalse(expr=self.target._is_connected)
        self.assertIsInstance(obj=self.target._is_connected, cls=bool)
        # transaction_in_progress
        self.assertEqual(
            first=self.target._transaction_in_progress,
            second=False,
        )
        self.assertIsInstance(obj=self.target._transaction_in_progress, cls=bool)

    @pytest.mark.unit
    def test_target_is_connected(
        self,
    ) -> None:
        """Test the Target is_connected property/function.

        Test if:
            1. Returns the expected value (in this test we expect it
            to be False because that is the default value when a Target
            instance is created).
        """
        # Change the value
        self.target._is_connected = True
        # Assert is_connected has the expected value
        self.assertTrue(expr=self.target.is_connected)
        # Change the value again
        self.target._is_connected = False
        # Assert is_connected has the expected value
        self.assertFalse(expr=self.target.is_connected)

    @patch(target="binance_api_fetcher.persistence.target.logger.debug")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_cursor_with_transaction_in_progress(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_debug: MagicMock,
    ) -> None:
        """Test the Target cursor property/function.

        Test if:
            1. Cursor returned is the same as the Target instance
            attribute.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_debug: Mock for the logger.debug
                function call.
        """
        # Set up attributes to meet conditions
        self.target._transaction_in_progress = True
        self.target._target_connection = mock_psycopg2_connect.return_value
        self.target._target_cursor = mock_psycopg2_connect.return_value.cursor

        # Call the function
        test_cursor = self.target.cursor

        # Assert that the logger.debug is called with the correct message
        mock_logger_debug.assert_called_with(msg="Using existing cursor.")
        # Assert that the test cursor is the same as the target_cursor
        self.assertEqual(first=test_cursor, second=self.target._target_cursor)

        # Tear Down - reset conditions that were set up for test
        self.target._transaction_in_progress = False
        del self.target._target_connection
        del self.target._target_cursor

    @patch(target="binance_api_fetcher.persistence.target.logger.debug")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_cursor_without_transaction_in_progress(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_debug: MagicMock,
    ) -> None:
        """Test the Target cursor property/function.

        Test if:
            1. Cursor returned is a new cursor.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_debug: Mock for the logger.debug
                function call.
        """
        # Set up attributes to meet conditions
        self.target._transaction_in_progress = False
        self.target._target_connection = mock_psycopg2_connect.return_value

        # Call the function
        test_cursor = self.target.cursor

        # Assert that the logger.debug is called with the correct message
        mock_logger_debug.assert_called_with(msg="Creating new cursor.")
        # Assert that the test cursor is the same as the return value of the cursor
        # function called by target_connection
        self.assertEqual(
            first=test_cursor,
            second=self.target._target_connection.cursor.return_value,
        )
        # Assert that cursor is called once
        self.target._target_connection.cursor.assert_called_once()

        # Tear Down - reset conditions that were set up for test
        del self.target._target_connection

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_cursor_psycopg2_error_handling(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target cursor property/function.

        Test if:
            1. Psycopg2 Error is caught and handled.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        self.target._target_connection = mock_psycopg2_connect.return_value
        self.target._target_connection.cursor.side_effect = psycopg2.Error(
            "Testing error"
        )

        # Call the cursor property/function
        with self.assertRaises(TargetError) as context:
            self.target.cursor

        # Assert that cursor is called once
        self.target._target_connection.cursor.assert_called_once()
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got a psycopg2 error while interacting with target datasource: "
            "Error - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error getting the postgres cursor.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=psycopg2.Error)

        # Tear Down - reset conditions that were set up for test
        del self.target._target_connection

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_cursor_exception_error_handling(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target cursor property/function.

        Test if:
            1. Exception is caught and handled.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        self.target._target_connection = mock_psycopg2_connect.return_value
        self.target._target_connection.cursor.side_effect = Exception("Testing error")

        # Call the cursor property/function
        with self.assertRaises(TargetError) as context:
            self.target.cursor

        # Assert that cursor is called once
        self.target._target_connection.cursor.assert_called_once()
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got an unexpected error while interacting with target datasource: "
            "Exception - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error getting the postgres cursor.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=Exception)

        # Tear Down - reset conditions that were set up for test
        del self.target._target_connection

    @patch(target="binance_api_fetcher.persistence.target.logger.info")
    @patch.object(target=Target, attribute="ping_datasource")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_connect_success(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_ping_datasource: MagicMock,
        mock_logger_info: MagicMock,
    ) -> None:
        """Test the Target connect function.

        Test if:
            1. Connect function is called and executes successfully.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_ping_datasource: Mock for the ping_datasource
                function call.
            mock_logger_info: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        mock_cursor: MagicMock = mock_psycopg2_connect.return_value.cursor

        # Call the connect function
        self.target.connect()

        # Assert that psycopg2 connect is called with args
        mock_psycopg2_connect.assert_called_once_with(
            dsn=self.target._connection_string
        )
        # Assert that target_connection has the value assigned
        self.assertEqual(
            first=self.target._target_connection,
            second=mock_psycopg2_connect.return_value,
        )
        # Assert that the mock_cursor is called once
        mock_cursor.assert_called_once()
        # Assert that target_cursor has the value assigned
        self.assertEqual(
            first=self.target._target_cursor,
            second=mock_cursor.return_value,
        )
        # Assert that ping_datasoruce is called once
        mock_ping_datasource.assert_called_once()
        # Assert is_connected has the expected value
        self.assertTrue(expr=self.target.is_connected)
        # Assert that the log is called correctly
        mock_logger_info.assert_called_with(
            msg=f"{self.target.__class__.__name__} connected to: "
            f"{mock_ping_datasource.return_value}."
        )

        # Tear Down - reset conditions that were updated for test
        self.target._is_connected = False
        del self.target._target_connection
        del self.target._target_cursor

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_connect_psycopg2_error_handling(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target connect function.

        Test if:
            1. Psycopg2 Error is caught and handled.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        mock_psycopg2_connect.side_effect = psycopg2.Error("Testing error")

        # Call the connect function
        with self.assertRaises(TargetError) as context:
            self.target.connect()

        # Assert that psycopg2 connect is called with args
        mock_psycopg2_connect.assert_called_once_with(
            dsn=self.target._connection_string
        )
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got a psycopg2 error while interacting with target datasource: "
            "Error - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error connecting with the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=psycopg2.Error)

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_connect_exception_error_handling(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target connect function.

        Test if:
            1. Exception is caught and handled.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        mock_psycopg2_connect.side_effect = Exception("Testing error")

        # Call the connect function
        with self.assertRaises(TargetError) as context:
            self.target.connect()

        # Assert that psycopg2 connect is called with args
        mock_psycopg2_connect.assert_called_once_with(
            dsn=self.target._connection_string
        )
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got an unexpected error while interacting with target datasource: "
            "Exception - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error connecting with the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=Exception)

    @patch.object(target=Target, attribute="cursor", new_callable=PropertyMock)
    @pytest.mark.unit
    def test_target_ping_datasource_with_fetchone_success(
        self,
        mock_cursor: MagicMock,
    ) -> None:
        """Test the Target ping_datasource function.

        Test if:
            1. Function is called and executes successfully
                with fetchone retrieving a Tuple.

        Args:
            mock_cursor: Mock for the cursor
                property/function call.
        """
        # Set up attributes to meet conditions
        mock_cursor.return_value.fetchone.return_value = ("Test success.",)

        # Call the ping_datasource function
        test_ping_datasource = self.target.ping_datasource()

        # Assert that mock_cursor is called once
        mock_cursor.assert_called_once()
        # Assert that execute is called with args
        mock_cursor.return_value.execute.assert_called_once_with(
            "SELECT CONCAT("
            "current_user,'@',inet_server_addr(),':',"
            "inet_server_port(),' - ',version()"
            ") as v"
        )
        # Assert that the fetchone is called once
        mock_cursor.return_value.fetchone.assert_called_once()
        # Assert that the test result is the value of the fetchone
        self.assertEqual(
            first=test_ping_datasource,
            second="Test success.",
        )

    @patch.object(target=Target, attribute="cursor", new_callable=PropertyMock)
    @pytest.mark.unit
    def test_target_ping_datasource_without_fetchone_success(
        self,
        mock_cursor: MagicMock,
    ) -> None:
        """Test the Target ping_datasource function.

        Test if:
            1. Function is called and executes successfully
                with fetchone retrieving None.

        Args:
            mock_cursor: Mock for the cursor
                property/function call.
        """
        # Set up attributes to meet conditions
        mock_cursor.return_value.fetchone.return_value = None

        # Call the ping_datasource function
        test_ping_datasource = self.target.ping_datasource()

        # Assert that mock_cursor is called once
        mock_cursor.assert_called_once()
        # Assert that execute is called with args
        mock_cursor.return_value.execute.assert_called_once_with(
            "SELECT CONCAT("
            "current_user,'@',inet_server_addr(),':',"
            "inet_server_port(),' - ',version()"
            ") as v"
        )
        # Assert that the fetchone is called once
        mock_cursor.return_value.fetchone.assert_called_once()
        # Assert that the test result is an empty string
        self.assertEqual(
            first=test_ping_datasource,
            second="",
        )

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch.object(target=Target, attribute="cursor", new_callable=PropertyMock)
    @pytest.mark.unit
    def test_target_ping_datasource_psycopg2_error_handling(
        self,
        mock_cursor: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target ping_datasource function.

        Test if:
            1. Psycopg2 Error is caught and handled.

        Args:
            mock_cursor: Mock for the cursor
                property/function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        mock_cursor.return_value.execute.side_effect = psycopg2.Error("Testing error")

        # Call the ping datasource function
        with self.assertRaises(TargetError) as context:
            self.target.ping_datasource()

        # Assert that mock_cursor is called once
        mock_cursor.assert_called_once()
        # Assert that execute is called with args
        mock_cursor.return_value.execute.assert_called_once_with(
            "SELECT CONCAT("
            "current_user,'@',inet_server_addr(),':',"
            "inet_server_port(),' - ',version()"
            ") as v"
        )
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got a psycopg2 error while interacting with target datasource: "
            "Error - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error pinging the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=psycopg2.Error)

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch.object(target=Target, attribute="cursor", new_callable=PropertyMock)
    @pytest.mark.unit
    def test_target_ping_datasource_exception_error_handling(
        self,
        mock_cursor: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target ping_datasource function.

        Test if:
            1. Exception is caught and handled.

        Args:
            mock_cursor: Mock for the cursor
                property/function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        mock_cursor.return_value.execute.side_effect = Exception("Testing error")

        # Call the ping datasource function
        with self.assertRaises(TargetError) as context:
            self.target.ping_datasource()

        # Assert that mock_cursor is called once
        mock_cursor.assert_called_once()
        # Assert that execute is called with args
        mock_cursor.return_value.execute.assert_called_once_with(
            "SELECT CONCAT("
            "current_user,'@',inet_server_addr(),':',"
            "inet_server_port(),' - ',version()"
            ") as v"
        )
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got an unexpected error while interacting with target datasource: "
            "Exception - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error pinging the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=Exception)

    @patch.object(target=Target, attribute="cursor", new_callable=PropertyMock)
    @pytest.mark.unit
    def test_target_begin_transaction(
        self,
        mock_cursor: MagicMock,
    ) -> None:
        """Test the Target begin  transaction function.

        Test if:
            1. A cursor is set as an attribute of target and
            the in progress control attribute is set to True.

        Args:
            mock_cursor: Mock for the cursor
                property/function call.
        """
        # Call the begin transaction function
        self.target.begin_transaction()

        # Assert that mock_cursor is called once
        mock_cursor.assert_called_once()
        # Assert that execute is called with args
        self.assertEqual(first=self.target._cursor, second=mock_cursor.return_value)
        # Assert that in_progress is set to True
        self.assertTrue(expr=self.target._transaction_in_progress)

        # Restore default values
        self.target._transaction_in_progress = False

    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_commit_transaction(
        self,
        mock_psycopg2_connect: MagicMock,
    ) -> None:
        """Test the Target commit transaction function.

        Test if:
            1. Transaction is committed, i.e. the psycopg2 function
            is called and the in_progress attribute is set to False.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
        """
        # Set up attributes to meet conditions
        self.target._target_connection = mock_psycopg2_connect.return_value

        # Call the function
        self.target.commit_transaction()

        # Assert that commit is called once
        self.target._target_connection.commit.assert_called_once()
        # Assert that in_progress is set to False
        self.assertFalse(expr=self.target._transaction_in_progress)

        # Tear Down - reset conditions that were set up for test
        del self.target._target_connection

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_commit_transaction_psycopg2_error_handling(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target commit transaction function.

        Test if:
            1. Psycopg2 Error is caught and handled.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        self.target._target_connection = mock_psycopg2_connect.return_value
        self.target._target_connection.commit.side_effect = psycopg2.Error(
            "Testing error"
        )

        # Call the commit transaction function
        with self.assertRaises(TargetError) as context:
            self.target.commit_transaction()

        # Assert that commit trannsaction is called once
        self.target._target_connection.commit.assert_called_once()
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got a psycopg2 error while interacting with target datasource: "
            "Error - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error commiting a transaction in the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=psycopg2.Error)

        # Tear Down - reset conditions that were set up for test
        del self.target._target_connection

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_commit_transaction_exception_error_handling(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target commit transaction function.

        Test if:
            1. Exception is caught and handled.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        self.target._target_connection = mock_psycopg2_connect.return_value
        self.target._target_connection.commit.side_effect = Exception("Testing error")

        # Call the commit transaction function
        with self.assertRaises(TargetError) as context:
            self.target.commit_transaction()

        # Assert that commit transaction is called once
        self.target._target_connection.commit.assert_called_once()
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got an unexpected error while interacting with target datasource: "
            "Exception - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error commiting a transaction in the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=Exception)

        # Tear Down - reset conditions that were set up for test
        del self.target._target_connection

    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_rollback_transaction(
        self,
        mock_psycopg2_connect: MagicMock,
    ) -> None:
        """Test the Target rollback transaction function.

        Test if:
            1. Transaction is committed, i.e. the psycopg2 function
            is called and the in_progress attribute is set to False.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
        """
        # Set up attributes to meet conditions
        self.target._target_connection = mock_psycopg2_connect.return_value

        # Call the function
        self.target.rollback_transaction()

        # Assert that rollback transaction is called once
        self.target._target_connection.rollback.assert_called_once()
        # Assert that in_progress is set to False
        self.assertFalse(expr=self.target._transaction_in_progress)

        # Tear Down - reset conditions that were set up for test
        del self.target._target_connection

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_rollback_transaction_psycopg2_error_handling(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target rollback transaction function.

        Test if:
            1. Psycopg2 Error is caught and handled.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        self.target._target_connection = mock_psycopg2_connect.return_value
        self.target._target_connection.rollback.side_effect = psycopg2.Error(
            "Testing error"
        )

        # Call the rollback transaction function
        with self.assertRaises(TargetError) as context:
            self.target.rollback_transaction()

        # Assert that rollback transaction is called once
        self.target._target_connection.rollback.assert_called_once()
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got a psycopg2 error while interacting with target datasource: "
            "Error - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error rolling back a transaction in the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=psycopg2.Error)

        # Tear Down - reset conditions that were set up for test
        del self.target._target_connection

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_rollback_transaction_exception_error_handling(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target rollback transaction function.

        Test if:
            1. Exception is caught and handled.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        self.target._target_connection = mock_psycopg2_connect.return_value
        self.target._target_connection.rollback.side_effect = Exception("Testing error")

        # Call the rollback transaction function
        with self.assertRaises(TargetError) as context:
            self.target.rollback_transaction()

        # Assert that rollback transaction is called once
        self.target._target_connection.rollback.assert_called_once()
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got an unexpected error while interacting with target datasource: "
            "Exception - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error rolling back a transaction in the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=Exception)

        # Tear Down - reset conditions that were set up for test
        del self.target._target_connection

    @patch(target="binance_api_fetcher.persistence.target.logger.info")
    @patch.object(target=Target, attribute="ping_datasource")
    @patch(target="binance_api_fetcher.persistence.target.psycopg2.connect")
    @pytest.mark.unit
    def test_target_disconnect_success(
        self,
        mock_psycopg2_connect: MagicMock,
        mock_ping_datasource: MagicMock,
        mock_logger_info: MagicMock,
    ) -> None:
        """Test the Target disconnect function.

        Test if:
            1. Disconnect function is called and executes successfully.

        Args:
            mock_psycopg2_connect: Mock for the psycopg2 connect
                function call.
            mock_ping_datasource: Mock for the ping_datasource
                function call.
            mock_logger_info: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        self.target._target_connection = mock_psycopg2_connect.return_value
        self.target._target_cursor = self.target._target_connection.cursor.return_value

        # Call the disconnect function
        self.target.disconnect()

        # Assert that ping_datasoruce is called once
        mock_ping_datasource.assert_called_once()
        # Assert that the  is called once
        self.target._target_cursor.close.assert_called_once()
        # Assert that psycopg2 connect is called with args
        self.target._target_connection.close.assert_called_once()
        # Assert transaction_in_progress has the expected value
        self.assertFalse(expr=self.target._transaction_in_progress)
        # Assert is_connected has the expected value
        self.assertFalse(expr=self.target.is_connected)
        # Assert that the log is called correctly
        mock_logger_info.assert_called_with(
            msg=f"{self.target.__class__.__name__} disconnected from: "
            f"{mock_ping_datasource.return_value}."
        )

        # Tear Down - reset conditions that were updated for test
        self.target._is_connected = False
        del self.target._target_connection
        del self.target._target_cursor

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch.object(target=Target, attribute="ping_datasource")
    @pytest.mark.unit
    def test_target_disconnect_psycopg2_error_handling(
        self,
        mock_ping_datasource: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target disconnect function.

        Test if:
            1. Psycopg2 Error is caught and handled.

        Args:
            mock_ping_datasource: Mock for the ping_datasource
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        mock_ping_datasource.side_effect = psycopg2.Error("Testing error")

        # Call the disconnect function
        with self.assertRaises(TargetError) as context:
            self.target.disconnect()

        # Assert that ping_datasource is called
        mock_ping_datasource.assert_called_once()
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got a psycopg2 error while interacting with target datasource: "
            "Error - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error disconnecting from the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=psycopg2.Error)

    @patch(target="binance_api_fetcher.persistence.target.logger.error")
    @patch.object(target=Target, attribute="ping_datasource")
    @pytest.mark.unit
    def test_target_disconnect_exception_error_handling(
        self,
        mock_ping_datasource: MagicMock,
        mock_logger_error: MagicMock,
    ) -> None:
        """Test the Target disconnect function.

        Test if:
            1. Exception is caught and handled.

        Args:
            mock_ping_datasource: Mock for the ping_datasource
                function call.
            mock_logger_error: Mock for the logger.error
                function call.
        """
        # Set up attributes to meet conditions
        mock_ping_datasource.side_effect = Exception("Testing error")

        # Call the disconnect function
        with self.assertRaises(TargetError) as context:
            self.target.disconnect()

        # Assert that ping datasource is called
        mock_ping_datasource.assert_called_once()
        # Assert that the logger.error is called with the correct message
        mock_logger_error.assert_called_with(
            msg="Got an unexpected error while interacting with target datasource: "
            "Exception - Testing error."
        )
        # Assert that the TargetError logs the correct message
        self.assertEqual(
            first=str(context.exception),
            second="Got an error disconnecting from the target datasource.",
        )
        # Assert the exception chaining (because we are already in Python 3.12)
        self.assertIsInstance(obj=context.exception.__cause__, cls=Exception)
