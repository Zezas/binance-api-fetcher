"""Test binance_api_fetcher StatusCode class."""

from unittest import TestCase

from binance_api_fetcher.model import StatusCode  # type: ignore
import pytest


class TestStatusCode(TestCase):
    """Class to test the StatusCode enum class.

    We use mocks for constructors and function calls to keep the
    unit tests isolated, i.e. we don't want to test the interaction
    between function calls and between classes.
    """

    @pytest.mark.unit
    def test_statuscode_members_and_values(self) -> None:
        """Test StatusCode members and values.

        Test if all members of the StatusCode class exist and have the
        expected values.
        """
        # Assert members
        self.assertTrue(StatusCode.OK in StatusCode)
        self.assertTrue(StatusCode.BAD_REQUEST in StatusCode)
        self.assertTrue(StatusCode.UNAUTHORIZED in StatusCode)
        self.assertTrue(StatusCode.FORBIDDEN in StatusCode)
        self.assertTrue(StatusCode.NOT_FOUND in StatusCode)
        self.assertTrue(StatusCode.METHOD_NOT_ALLOWED in StatusCode)
        self.assertTrue(StatusCode.NOT_ACCEPTABLE in StatusCode)
        self.assertTrue(StatusCode.TOO_MANY_REQUESTS in StatusCode)
        self.assertTrue(StatusCode.INTERNAL_SERVER_ERROR in StatusCode)
        self.assertTrue(StatusCode.BAD_GATEWAY in StatusCode)
        self.assertTrue(StatusCode.SERVICE_UNAVAILABLE in StatusCode)
        self.assertTrue(StatusCode.GATEWAY_TIMEOUT in StatusCode)
        # Assert values
        self.assertEqual(StatusCode.OK.value, 200)
        self.assertEqual(StatusCode.BAD_REQUEST.value, 400)
        self.assertEqual(StatusCode.UNAUTHORIZED.value, 401)
        self.assertEqual(StatusCode.FORBIDDEN.value, 403)
        self.assertEqual(StatusCode.NOT_FOUND.value, 404)
        self.assertEqual(StatusCode.METHOD_NOT_ALLOWED.value, 405)
        self.assertEqual(StatusCode.NOT_ACCEPTABLE.value, 406)
        self.assertEqual(StatusCode.TOO_MANY_REQUESTS.value, 429)
        self.assertEqual(StatusCode.INTERNAL_SERVER_ERROR.value, 500)
        self.assertEqual(StatusCode.BAD_GATEWAY.value, 502)
        self.assertEqual(StatusCode.SERVICE_UNAVAILABLE.value, 503)
        self.assertEqual(StatusCode.GATEWAY_TIMEOUT.value, 504)

    @pytest.mark.unit
    def test_enum_repr(self) -> None:
        """Test the StatusCode __repr__ function.

        Test if the function call has the expected value for all
        members of the StatusCode class.
        """
        self.assertEqual(repr(StatusCode.OK), "200")
        self.assertEqual(repr(StatusCode.BAD_REQUEST), "400")
        self.assertEqual(repr(StatusCode.UNAUTHORIZED), "401")
        self.assertEqual(repr(StatusCode.FORBIDDEN), "403")
        self.assertEqual(repr(StatusCode.NOT_FOUND), "404")
        self.assertEqual(repr(StatusCode.METHOD_NOT_ALLOWED), "405")
        self.assertEqual(repr(StatusCode.NOT_ACCEPTABLE), "406")
        self.assertEqual(repr(StatusCode.TOO_MANY_REQUESTS), "429")
        self.assertEqual(repr(StatusCode.INTERNAL_SERVER_ERROR), "500")
        self.assertEqual(repr(StatusCode.BAD_GATEWAY), "502")
        self.assertEqual(repr(StatusCode.SERVICE_UNAVAILABLE), "503")
        self.assertEqual(repr(StatusCode.GATEWAY_TIMEOUT), "504")
