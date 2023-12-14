"""Test binance_api_fetcher Source class."""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from binance_api_fetcher.persistence import Source, SourceError
import pytest
import requests
from requests import Response


class TestSource(TestCase):
    """Class to test the Source class functions.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.

    Attributes:
        source: Source class instance that will be used in every unit test.
        test_connection_string: String used to create the Source instance.
    """

    source: Source
    test_connection_string: str

    def setUp(self) -> None:
        """Create a source instance to use in all tests.

        We use the mocks in order to prevent the Source constructor
        to call functions, so we can use and test them, otherwise we
        have ValueErrors because of the packages that should not be
        addressed by these tests.
        """
        # Create a connection string used by the target
        self.test_connection_string: str = "https://api.binance.com/api/v3/"
        # Set up a Source instance for all tests (call the __init__ function)
        self.source = Source(connection_string=self.test_connection_string)

    @pytest.mark.unit
    def test_source_init(
        self,
    ) -> None:
        """Test the Source __init__ function.

        Test if:
            1. Attributes of the Source instance have the args
            received and default values assigned.
        """
        # url
        self.assertEqual(
            first=self.source._url,
            second=self.test_connection_string,
        )
        self.assertIsInstance(obj=self.source._url, cls=str)

    @pytest.mark.unit
    def test_source_ping_url(
        self,
    ) -> None:
        """Test the Source ping_url property/function.

        Test if:
            1. Returns the expected value.
        """
        # Create the expected ping url
        expected_ping_url: str = "ping"

        # Assert ping_url has the expected value
        self.assertEqual(
            first=self.source.ping_url,
            second=expected_ping_url,
        )

    @patch(target="binance_api_fetcher.persistence.source.logger.info")
    @patch.object(target=Source, attribute="request")
    @pytest.mark.unit
    def test_source_connect_without_error(
        self,
        mock_request: MagicMock,
        mock_logger_info: MagicMock,
    ) -> None:
        """Test the Source connect function without error.

        Test if:
            1. The call to the request function is made with the
            correct arguments;
            2. The sucess message is logged.

        Args:
            mock_request: Mock for request function call.
            mock_logger_info: Mock for logger.info function call.
        """
        # Mock the request function to return a successful response
        mock_response: MagicMock = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        # Call the connect function
        self.source.connect()

        # Assert request is called with the correct arguments
        mock_request.assert_called_once_with(url=self.source.ping_url)

        # Assert logger.info is called with the correct message
        mock_logger_info.assert_called_with(
            msg=f"{self.source.__class__.__name__} " f"connected to: {self.source._url}"
        )

    @patch(target="binance_api_fetcher.persistence.source.logger.info")
    @patch.object(target=Source, attribute="request")
    @pytest.mark.unit
    def test_source_connect_with_error(
        self,
        mock_request: MagicMock,
        mock_logger_info: MagicMock,
    ) -> None:
        """Test the Source connect function with error.

        Test if:
            1. The call to the request function is made with the
            correct arguments;
            2. The error is raised;
            3. The error message is correct;
            4. The logger is not called.

        Args:
            mock_request: Mock for request function call.
            mock_logger_info: Mock for logger.info function call.
        """
        # Mock the request function to return a unsuccessful response
        mock_response: MagicMock = MagicMock(spec=Response)
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_request.return_value = mock_response

        # Call the connect function, expecting a SourceError
        with self.assertRaises(SourceError) as context:
            self.source.connect()

        # Assert request is called with the correct arguments
        mock_request.assert_called_once_with(url=self.source.ping_url)

        # Assert the error message
        self.assertEqual(
            first=str(context.exception),
            second=(
                "Error connecting to source: "
                f"{mock_response.status_code} - {mock_response.text}."
            ),
        )

        # Assert logger.info is not called
        mock_logger_info.assert_not_called()

    @patch(target="binance_api_fetcher.persistence.source.logger.warning")
    @patch(target="binance_api_fetcher.persistence.source.requests")
    @pytest.mark.unit
    def test_source_request_without_error(
        self,
        mock_requests_get: MagicMock,
        mock_logger_warning: MagicMock,
    ) -> None:
        """Test the Source request function without error.

        Test if:
            1. The call to the requests.get function is made with the
            correct arguments;
            2. The response from the request is returned.
            3. The logger is not called.

        Args:
            mock_requests_get: Mock for requests.get function call.
            mock_logger_warning: Mock for logger.warning function call.
        """
        # Create a test url to use as argument for the request function
        test_url: str = "test_url"
        # Mock the requests.get function to return a successful response
        mock_response: MagicMock = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_requests_get.get.return_value = mock_response

        # Call the request function
        request_result = self.source.request(url=test_url)

        # Assert request is called with the correct arguments
        mock_requests_get.get.assert_called_once_with(
            url=self.source._url + test_url, params=None, timeout=120
        )

        # Assert the response is returned with the expected result
        self.assertEqual(first=request_result, second=mock_response)

        # Assert logger.warning is not called
        mock_logger_warning.assert_not_called()

    @patch(target="binance_api_fetcher.persistence.source.logger.warning")
    @patch(target="binance_api_fetcher.persistence.source.requests.get")
    @pytest.mark.unit
    def test_source_request_with_error(
        self,
        mock_requests_get: MagicMock,
        mock_logger_warning: MagicMock,
    ) -> None:
        """Test the Source request function with error.

        Test if:
            1. The call to the requests.get function is made with the
            correct arguments;
            2. The warning message is correct;
            3. A default response is returned.

        Args:
            mock_requests_get: Mock for requests.get function call.
            mock_logger_warning: Mock for logger.warning function call.
        """
        # Create a test url to use as argument for the request function
        test_url: str = "test_url"
        # Create a side effect for the requests.get to get an Exception
        mock_requests_get.side_effect = requests.exceptions.RequestException(
            "Testing error"
        )

        # Call the request function
        request_result = self.source.request(url=test_url)

        # Assert request is called with the correct arguments
        mock_requests_get.assert_called_once_with(
            url=self.source._url + test_url, params=None, timeout=120
        )

        # Assert logger.warning is called with the correct message
        mock_logger_warning.assert_called_with(
            "Error making request: " "RequestException - Testing error."
        )

        # Assert the response returned is stil a requests.Response
        self.assertIsInstance(obj=request_result, cls=Response)
