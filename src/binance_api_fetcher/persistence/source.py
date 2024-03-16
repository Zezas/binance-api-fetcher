"""Source data source."""

import logging
from typing import Dict, Optional, Union

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
    # Bool to know if connection to source is exists
    _is_connected: bool

    def __init__(self, connection_string: str) -> None:
        """Initialize source components.

        Create a class instance with the connection string received
        and set the defaults for the attributes needed.

        Args:
            connection_string: Definitions to connect to the data source.
        """
        self._url = connection_string
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
        # TODO this should be configured
        return "ping"

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
        # TODO put status codes in a constants file
        if ping_response.status_code == 200:
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
        """
        try:
            # TODO put request timeout as env variable
            response: Response = requests.get(
                url=self._url + url, params=params, timeout=120
            )

        except requests.exceptions.RequestException as request_error:
            logger.warning(
                msg="Error making request: "
                f"{type(request_error).__name__} - {request_error}."
            )
            return requests.Response()
        # TODO add generic Exception handle

        return response

    def disconnect(self) -> None:
        """Disconnect from data source.

        Set the is_connected attribute to False
        and log a message.
        """
        self._is_connected = False
        logger.info(msg=f"{self.__class__.__name__} disconnected from: {self._url}.")
