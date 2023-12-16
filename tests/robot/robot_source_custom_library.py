"""Robot custom library for the Source class."""

from binance_api_fetcher.persistence import Source


def create_source_instance(connection_string: str) -> Source:
    """Create Source class instance.

    Create a Source class instance with the connection string received.

    Args:
        connection_string: Definitions to connect to the data source.

    Returns:
        Source: Source class instance.
    """
    return Source(connection_string)


def connect_to_source(source: Source) -> None:
    """Connect Source component to data source.

    Make a "ping" request to check if there is a connection.
    Logs a success message or raises an error.

    Args:
        source: Source class instance.
    """
    source.connect()
