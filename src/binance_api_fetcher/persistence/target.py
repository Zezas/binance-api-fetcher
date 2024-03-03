"""Target data source."""

import logging
from typing import Optional, Tuple

import psycopg2
from psycopg2.extensions import connection as Connection, cursor as Cursor

logger = logging.getLogger(__name__)


class TargetError(Exception):
    """Target error.

    Raised when we have an unexpected behaviour in the Target class.
    """

    pass


class Target:
    """Target component class.

    This class is responsible to fetch and persist data to a target.
    """

    # Connection to the data source
    _target_connection: Connection
    # Cursor for the data source
    _target_cursor: Cursor
    # String with the definitions to connect to the data source
    _connection_string: str
    # Bool to know if connection to target is exists
    _is_connected: bool
    # Bool to know if a transaction is in progress
    _transaction_in_progress: bool

    def __init__(self, connection_string: str) -> None:
        """Initialize target components.

        Create a class instance with the connection string received
        and set the defaults for the attributes needed.

        Args:
            connection_string: Definitions to connect with data source.
        """
        self._connection_string: str = connection_string
        self._is_connected = False
        self._transaction_in_progress: bool = False

    @property
    def is_connected(self) -> bool:
        """Attribute to know if target is connected.

        Returns:
            bool: True if target is connected.
        """
        return self._is_connected

    @property
    def cursor(self) -> Cursor:
        """Gets postgres cursor.

        If a transaction is in progress and the cursor already
        exists (i.e. is not Null), then the returned cursor is the
        existing one. Otherwise, a new psycopg2 cursor is created.

        Returns:
            Cursor: Psycopg2 cursor.

        Raises:
            TargetError: Raised when an error occurs while
                interacting with target.
        """
        try:
            if self._transaction_in_progress:
                logger.debug(msg="Using existing cursor.")
                return self._target_cursor

            logger.debug(msg="Creating new cursor.")
            return self._target_connection.cursor()
        except psycopg2.Error as error:
            logger.error(
                msg=f"Got a psycopg2 error while interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError("Got an error getting the postgres cursor.") from error
        except Exception as error:
            logger.error(
                msg=f"Got an unexpected error while "
                "interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError("Got an error getting the postgres cursor.") from error

    def connect(self) -> None:
        """Connects to target datasource.

        After connecting, set the autocommit to False, create a default cursor
        and ping the datasource in order to confirm the connection is successful.

        Raises:
            TargetError: Raised when an error occurs while
                interacting with target.
        """
        try:
            # Set up the connection
            self._target_connection = psycopg2.connect(dsn=self._connection_string)
            # Create a default cursor
            self._target_cursor = self._target_connection.cursor()
            # Ping the datasource
            url: str = self.ping_datasource()
            # Connection is successful
            self._is_connected = True
            logger.info(msg=f"{self.__class__.__name__} connected to: {url}.")
        except psycopg2.Error as error:
            logger.error(
                msg=f"Got a psycopg2 error while interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError(
                "Got an error connecting with the target datasource."
            ) from error
        except Exception as error:
            logger.error(
                msg=f"Got an unexpected error while "
                "interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError(
                "Got an error connecting with the target datasource."
            ) from error

    def ping_datasource(self) -> str:
        """Pings data source.

        Query the target datasource to fetch the connection
        information, to make sure the connection to the target
        datasource is successful.

        Returns:
            str: String with target datasource connection information.

        Raises:
            TargetError: Raised when an error occurs while
                interacting with target.
        """
        try:
            # self.begin_transaction()
            cursor: Cursor = self.cursor
            cursor.execute(
                "SELECT CONCAT("
                "current_user,'@',inet_server_addr(),':',"
                "inet_server_port(),' - ',version()"
                ") as v"
            )
            result: Optional[Tuple] = cursor.fetchone()
            # self.commit_transaction()

            ping_response: str = result[0] if result is not None else ""

            return ping_response
        except psycopg2.Error as error:
            logger.error(
                msg=f"Got a psycopg2 error while interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError("Got an error pinging the target datasource.") from error
        except Exception as error:
            logger.error(
                msg=f"Got an unexpected error while "
                "interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError("Got an error pinging the target datasource.") from error

    def begin_transaction(self) -> None:
        """Begins a transaction.

        By default, with psycopg2 the BEGIN TRANSACTION statement is always
        executed. So in this function, we just need to create make sure a cursor
        is attributed to our object's cursor, and set the in_progress control
        attribute to true.
        """
        self._cursor = self.cursor
        self._in_progress = True

    def commit_transaction(self) -> None:
        """Commits a transaction.

        Call the commit function of the psycopg2 library and
        set the in_progress control attribute to false.

        Raises:
            TargetError: Raised when an error occurs while
                interacting with target.
        """
        try:
            self._target_connection.commit()
            self._in_progress = False
        except psycopg2.Error as error:
            logger.error(
                msg=f"Got a psycopg2 error while interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError(
                "Got an error commiting a transaction in the target datasource."
            ) from error
        except Exception as error:
            logger.error(
                msg=f"Got an unexpected error while "
                "interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError(
                "Got an error commiting a transaction in the target datasource."
            ) from error

    def rollback_transaction(self) -> None:
        """Rolls back a transaction.

        Call the rollback function of the psycopg2 library and
        set the in_progress control attribute to false.

        Raises:
            TargetError: Raised when an error occurs while
                interacting with target.
        """
        try:
            self._target_connection.rollback()
            self._in_progress = False
        except psycopg2.Error as error:
            logger.error(
                msg=f"Got a psycopg2 error while interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError(
                "Got an error rolling back a transaction in the target datasource."
            ) from error
        except Exception as error:
            logger.error(
                msg=f"Got an unexpected error while "
                "interacting with target datasource: "
                f"{type(error).__name__} - {error}."
            )
            raise TargetError(
                "Got an error rolling back a transaction in the target datasource."
            ) from error

    # def disconnect(self) -> None:
    #     """Disconnects data source connection."""
    #     url = self.ping_datasource()
    #     self._connection.close()
    #     self._in_progress = False
    #     logger.info(f"{self.__class__.__name__} disconnected from: {url}")

    # def get_next_delivery_id(self) -> int:
    #     """Gets next delivery id.

    #     Returns:
    #         Next delivery id.
    #     """
    #     cursor = self.cursor
    #     # ALTER SEQUENCE delivery_id_delivery_api_seq RESTART;
    #     cursor.execute("SELECT NEXTVAL('delivery_id_delivery_api_seq');")
    #     res = cursor.fetchone()

    #     return res[0]

    # def get_next_event_id(self, n: int = 1) -> Iterator[int]:
    #     """Gets next event id.

    #     Args:
    #         n: Number of event ids to get.

    #     Yields:
    #         Next event id.
    #     """
    #     cursor = self.cursor
    #     # ALTER SEQUENCE event_id_delivery_s3_seq RESTART;
    #     cursor.execute(
    #         "SELECT NEXTVAL('event_id_delivery_api_seq') "
    #         "FROM GENERATE_SERIES(1, %(n_event_ids)s);",
    #         vars={"n_event_ids": n},
    #     )

    #     event_id = cursor.fetchone()
    #     while event_id is not None:
    #         yield event_id[0]
    #         event_id = cursor.fetchone()

    # def get_symbols(
    #     self, query: Optional[str], shard: int
    # ) -> List[Tuple[Optional[str], Optional[datetime]]]:
    #     """Gets entity symbols.

    #     Args:
    #         query: Query to fetch entity symbols.
    #         shard: Shard of symbols to fetch.

    #     Returns:
    #         Entity symbols.
    #     """
    #     if query is None:
    #         return [(None, None)]

    #     cursor = self.cursor
    #     cursor.execute(query=query, vars={"shard": shard})
    #     res = cursor.fetchall()

    #     return res

    # def get_current_state(self, query: str, args: Keys) -> List[Tuple]:
    #     """Gets current state of entity records.

    #     Args:
    #         query: Query to fetch entity current state records.
    #         args: List of tuples, each containing a key of corresponding entity
    #             to fetch state.

    #     Returns:
    #         Current state of entity records.
    #     """
    #     cursor = self.cursor
    #     records = execute_values(cur=cursor, sql=query, argslist=args, fetch=True)

    #     return records

    # def persist_delivery(self, args: Dict[str, Any]) -> None:
    #     """Persist delivery state.

    #     Args:
    #         args: Delivery metadata to persist.
    #     """
    #     query = (
    #         "INSERT INTO loader_delivery_api ("
    #         "delivery_id, "
    #         "entity, "
    #         "shard, "
    #         "row_creation, "
    #         "summary, "
    #         "runtime"
    #         ") VALUES ("
    #         "%(delivery_id)s, "
    #         "%(entity)s, "
    #         "%(shard)s, "
    #         "%(row_creation)s, "
    #         "%(summary)s, "
    #         "%(runtime)s"
    #         ");"
    #     )
    #     cursor = self.cursor
    #     cursor.execute(query=query, vars=args)

    # def execute(self, instruction: str, logs: List[Tuple]) -> None:
    #     """Executes an instruction (CREATE, AMEND, REMOVE) for given logs.

    #     Args:
    #         instruction: Instruction to execute (CREATE, AMEND, REMOVE).
    #         logs: Event logs to apply in instruction.
    #     """
    #     if logs:
    #         cursor = self.cursor
    #         execute_values(cur=cursor, sql=instruction, argslist=logs)
