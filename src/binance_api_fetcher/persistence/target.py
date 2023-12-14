"""Target data source."""

import logging

from psycopg2.extensions import connection as Connection, cursor as Cursor

logger = logging.getLogger(__name__)


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
        self._transaction_in_progress: bool = False

    # @property
    # def cursor(self) -> psycopg2.extensions.cursor:
    #     """Gets postgres cursor."""
    #     if self._transaction_in_progress and self._cursor is not None:
    #         cursor = self._cursor
    #     else:
    #         cursor = self._connection.cursor()

    #     return cursor

    # def connect(self) -> None:
    #     """Connects to data source."""
    #     self._connection = psycopg2.connect(dsn=self._connection_string)
    #     self._connection.autocommit = False
    #     url = self.ping_datasource()
    #     logger.info(f"{self.__class__.__name__} connected to: {url}")

    # def ping_datasource(self) -> str:
    #     """Pings data source."""
    #     cursor = self.cursor
    #     cursor.execute(
    #         "SELECT CONCAT("
    #         "current_user,'@',inet_server_addr(),':',"
    #         "inet_server_port(),' - ',version()"
    #         ") as v"
    #     )

    #     return cursor.fetchone()[0]

    # def begin_transaction(self) -> None:
    #     """Begins a transaction."""
    #     self._cursor = self.cursor
    #     self._in_progress = True

    # def commit_transaction(self) -> None:
    #     """Commits a transaction."""
    #     self._connection.commit()
    #     self._in_progress = False

    # def rollback_transaction(self) -> None:
    #     """Rolls back a transaction."""
    #     self._connection.rollback()
    #     self._in_progress = False

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
