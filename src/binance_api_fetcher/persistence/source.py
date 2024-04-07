"""Source data source."""

import logging
from typing import Dict, Optional, Union

from binance_api_fetcher.model import StatusCode
import requests
from requests import Response

logger = logging.getLogger(__name__)


class SourceError(Exception):
    """Source error.

    Raised when we have an unexpected behaviour in the Source class.
    """

    pass


class Source:
    """Source component class.

    This class is responsible to fetch data from a source.
    """

    # String with the url used to fetch data
    _url: str
    # String with the ping information
    _ping: str
    # Int with the request timeout (seconds)
    _request_timeout: int
    # Bool to know if connection to source is exists
    _is_connected: bool

    def __init__(
        self,
        connection_string: str,
        ping_string: str,
        request_timeout: int,
    ) -> None:
        """Initialize source components.

        Create a class instance with the connection string received
        and set the defaults for the attributes needed.

        Args:
            connection_string: Definitions to connect to the data source.
            ping_string: Definitions to ping the data source.
            request_timeout: Request timeout to fetch data from the data source.
        """
        self._url = connection_string
        self._ping = ping_string
        self._request_timeout = request_timeout
        self._is_connected = False

    @property
    def is_connected(self) -> bool:
        """Attribute to know if source is connected.

        Returns:
            bool: True if source is connected.
        """
        return self._is_connected

    @property
    def ping_url(self) -> str:
        """Ping endpoint url.

        Returns:
            str: Ping endpoint url.
        """
        return self._ping

    def connect(self) -> None:
        """Connect to data source.

        Make a "ping" request and validate the response status code.
        Finally, log a success message or raise an error if it fails.

        Raises:
            SourceError: Raised when an error occurs while
                connecting to source.
        """
        # Make the ping request
        ping_response: Response = self.request(url=self.ping_url)
        # Check the status code
        if ping_response.status_code == StatusCode.OK.value:
            self._is_connected = True
            logger.info(msg=f"{self.__class__.__name__} connected to: {self._url}.")
        else:
            self._is_connected = False
            raise SourceError(
                "Error connecting to source: "
                f"{ping_response.status_code} - {ping_response.text}."
            )

    def request(
        self, url: str, params: Optional[Dict[str, Union[str, int]]] = None
    ) -> Response:
        """Makes request to source API.

        Args:
            url: URL endpoint to make request.
            params: Request parameters.

        Returns:
            Response: API response.

        Raises:
            SourceError: Raised when an error occurs while
                interacting with source.
        """
        try:
            response: Response = requests.get(
                url=self._url + url, params=params, timeout=self._request_timeout
            )
            return response
        except requests.exceptions.RequestException as error:
            logger.warning(
                msg=f"Error making request: {type(error).__name__} - {error}."
            )
            return requests.Response()
        except Exception as error:
            logger.error(
                msg=f"Got an unexpected error while "
                "interacting with source datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise SourceError(
                "Got an error requesting the source datasource."
            ) from error

    def disconnect(self) -> None:
        """Disconnect from data source.

        Set the is_connected attribute to False
        and log a message.
        """
        self._is_connected = False
        logger.info(msg=f"{self.__class__.__name__} disconnected from: {self._url}.")
