"""Service class."""

# import argparse
# import ast
# from datetime import datetime
# import json
# import logging
# import os
# import secrets
# from sys import stdout
# import time
# from typing import (
#     Dict,
#     List,
#     Optional,
#     Set,
#     Tuple,
#     Type,
# )

# import requests

# # from binance_api_fetcher import __version__
# # from binance_api_fetcher._constants import (
# #     BASE_ASSET,
# #     BASE_ASSET_DACS_RANK,
# #     CLOSE,
# #     CLOSE_TIME,
# #     HIGH,
# #     IGNORED,
# #     LOW,
# #     NUMBER_OF_TRADES,
# #     OPEN,
# #     OPEN_TIME,
# #     QUOTE_ASSET,
# #     QUOTE_ASSET_DACS_RANK,
# #     QUOTE_ASSET_VOLUME,
# #     SYMBOL,
# #     TAKER_BUY_BASE_ASSET_VOLUME,
# #     TAKER_BUY_QUOTE_ASSET_VOLUME,
# #     VOLUME,
# # )
# # from binance_api_fetcher._encoders import MessagesEncoder
# # from binance_api_fetcher._types import Key, Keys, Record
# # from binance_api_fetcher.endpoint import KlineEndpoint, SymbolEndpoint
# # from binance_api_fetcher.endpoint.base import Endpoint
# # from binance_api_fetcher.messaging import publisher
# # import binance_api_fetcher.model as model
# # from binance_api_fetcher.model.base import EventLog, State
# # from binance_api_fetcher.model.entity import Entity
# # from binance_api_fetcher.model.event_type import EventType
# # from binance_api_fetcher.persistance import source, target
# # import binance_api_fetcher.queries as queries
# # from binance_api_fetcher.queries.base import BaseQueries

# logger = logging.getLogger(__name__)

# # Events = Dict[EventType, List[EventLog]]
# # Delivery = Dict[Entity, Events]
# # Summary = Dict[Entity, Dict[EventType, int]]


# class ServiceError(Exception):
#     """Raised when we have unexpected behaviour in the Service class."""

#     pass


# class Service:
#     """Service class."""

#     # _source: source.Source
#     # _target: target.Target
#     # _notifier: publisher.Notifier
#     # _notifications: bool
#     # _dry_run: bool
#     # _min_sleep: int
#     # _max_sleep: int
#     # _batch_size: int
#     # _shard: int

#     # _entities: Set[Entity] = set()
#     # _endpoints: Dict[Entity, Endpoint] = {
#     #     Entity.KLINE_1D: KlineEndpoint(interval="1d"),
#     #     Entity.SYMBOL: SymbolEndpoint(),
#     # }
#     # _queries: Dict[Entity, BaseQueries] = {
#     #     Entity.KLINE_1D: queries.Kline1dQueries(),
#     #     Entity.SYMBOL: queries.SymbolQueries(),
#     # }
#     # _state: Dict[Entity, Type[State]] = {
#     #     Entity.KLINE_1D: model.Kline1d,
#     #     Entity.SYMBOL: model.Symbol,
#     # }
#     # _event_log: Dict[Entity, Type[EventLog]] = {
#     #     Entity.KLINE_1D: model.Kline1dLog,
#     #     Entity.SYMBOL: model.SymbolLog,
#     # }

#     _status_codes: Dict[int, str] = {
#         200: "OK",
#         400: "Bad Request",
#         401: "Unauthorized",
#         403: "Forbidden",
#         404: "Not Found",
#         405: "Method Not Allowed",
#         406: "Not Acceptable",
#         429: "Too Many Requests",
#         500: "Internal Server Error",
#         502: "Bad Gateway",
#         503: "Service Unavailable",
#         504: "Gateway Timeout",
#     }

#     # def setup(self, args: argparse.Namespace) -> None:
#     #     """Prepares loader components.

#     #     Args:
#     #         args: Variables given by user when starting loader process.

#     #     Connects to source, all possible targets and notification components.
#     #     """
#     #     self._notifications = args.notifications
#     #     self._dry_run = args.dry_run
#     #     self._min_sleep = args.min_sleep
#     #     self._max_sleep = args.max_sleep
#     #     self._batch_size = args.batch_size
#     #     self._shard = args.shard

#     #     if args.kline_1d:
#     #         self._entities.add(Entity.KLINE_1D)
#     #     if args.symbol:
#     #         self._entities.add(Entity.SYMBOL)

#     #     # prepare persistence FROM
#     #     self._source = source.Source(args.source)

#     #     # prepare persistence
#     #     self._target = target.Target(args.target)

#     #     # prepare notifier
#     #     if self._notifications:
#     #         self._notifier = publisher.Notifier(
#     #             datasource="binance",
#     #             loader_id="delivery-api",
#     #             url=args.nats,
#     #         )

#     #     # prepare prometheus
#     #     self.declare_metrics()

#     # def tear_down(self) -> None:
#     #     """Cleans loader settings.

#     #     Disconnects from source, target and notification components.
#     #     """
#     #     # cleanup and leave
#     #     self._source.disconnect()
#     #     self._target.disconnect()

#     #     if self._notifications:
#     #         self._notifier.disconnect()

#     # def run(self, args: argparse.Namespace) -> None:
#     #     """Checks the command line arguments for execution type.

#     #     This process can be executed as a service or just once.

#     #     Args:
#     #         args: Variables given by user when starting loader process.
#     #     """
#     #     logger.info(f"binance-delivery-api v{__version__}")

#     #     self.setup(args=args)

#     #     self._source.connect()
#     #     self._target.connect()
#     #     if self._notifications:
#     #         self._notifier.connect()

#     #     # type of execution
#     #     if args.run_as_service:
#     #         self.run_service()
#     #     else:
#     #         self.run_once()

#     #     self.tear_down()

#     # def run_service(self) -> None:
#     #     """Runs the application as a continuous process.

#     #     Polls the source every X seconds for new records.
#     #     Once new records are found, operations are applied to the "target" components.  # noqa: B950
#     #     """
#     #     logger.info(
#     #         f"Running as a service. "
#     #         f"source_polling_interval=[{self._min_sleep},{self._max_sleep}]."
#     #     )

#     #     continue_watching_folder = True
#     #     while continue_watching_folder:
#     #         try:
#     #             self.run_once()
#     #             t = secrets.choice(
#     #                 [self._min_sleep, self._max_sleep]
#     #                 + [i for i in range(self._min_sleep, self._max_sleep)]
#     #             )
#     #             time.sleep(t)
#     #         except Exception as e:
#     #             logger.warning("error while importing:", e)
#     #             continue_watching_folder = False

#     #     logger.info("Terminating...")

#     # def run_once(self) -> None:
#     #     """Runs the synchronization process once."""
#     #     start_time: datetime = datetime.utcnow()
#     #     end_time: datetime

#     #     entity: Entity = secrets.choice(list(self._entities))

#     #     records: List[Record] = self.scrape(entity=entity)

#     #     if not records:
#     #         end_time = datetime.utcnow()
#     #         logger.debug(f"No files to process: {end_time - start_time} seconds.")
#     #         return

#     #     delivery_id: int = self._target.get_next_delivery_id()
#     #     delivery: Delivery = {
#     #         entity: self.process(
#     #             delivery_id=delivery_id, entity=entity, records=records
#     #         )
#     #     }

#     #     # persist delivery
#     #     if not self._dry_run:
#     #         self.persist_delivery(
#     #             delivery_id=delivery_id,
#     #             entity=entity,
#     #             start_time=start_time,
#     #             delivery=delivery,
#     #         )

#     #     if self._notifications:
#     #         self.publish_messages(delivery_id=delivery_id, delivery=delivery)

#     #     self.increment_counters(delivery_id=delivery_id, delivery=delivery)

#     #     del delivery, records

#     #     end_time = datetime.utcnow()
#     #     logger.info(
#     #         f"Delivery {delivery_id}: processed ({end_time - start_time} seconds)."
#     #     )

#     # def scrape(self, entity: Entity) -> List[Record]:
#     #     """Scrapes based on entity received.

#     #     Args:
#     #         entity: Entity to scrape.

#     #     Returns:
#     #         Records scraped.
#     #     """
#     #     logger.info(f"Entity {entity}: scraping with shard {self._shard}...")

#     #     delivery: List[Record] = []
#     #     endpoint: Endpoint = self._endpoints[entity]

#     #     query = endpoint.query_select_symbols
#     #     symbols = self._target.get_symbols(query=query, shard=self._shard)

#     #     # for each symbol scrape
#     #     for index, s in enumerate(symbols, start=1):
#     #         logger.info(
#     #             f"Entity {entity}: scraping {index}/{len(symbols)} "
#     #             f"with shard {self._shard}..."
#     #         )
#     #         response: requests.Response = self._source.request(
#     #             url=endpoint.url,
#     #             params=endpoint.parameters(
#     #                 symbol=s[0], start_time=s[1], limit=self._batch_size
#     #             ),
#     #         )

#     #         self.increment_status_code(entity=entity, status_code=response.status_code)  # noqa: B950

#     #         if response.status_code != 200:
#     #             logger.warning(
#     #                 f"Entity {entity}: {response.status_code} {response.text}"
#     #             )
#     #             return delivery

#     #         records = self.parse(entity=entity, response=response, symbol=s[0])

#     #         delivery.extend(records)

#     #         # sleep between api calls
#     #         t = secrets.choice(
#     #             [self._min_sleep, self._max_sleep]
#     #             + [i for i in range(self._min_sleep, self._max_sleep)]
#     #         )
#     #         time.sleep(t)

#     #     return delivery

#     # def parse(
#     #     self, entity: Entity, response: requests.Response, symbol: Optional[str]
#     # ) -> List[Record]:
#     #     """Parses response received.

#     #     Args:
#     #         entity: Entity scraped.
#     #         response: Response from scraping.
#     #         symbol: Symbol asked in scraping.

#     #     Returns:
#     #         List of records parsed from response.
#     #     """
#     #     logger.info(f"Entity {entity}: parsing data scraped...")

#     #     try:
#     #         records = json.loads(response.text)
#     #     except json.JSONDecodeError:
#     #         logger.warning(f"Entity {entity}: can't load data scraped...")
#     #         return []

#     #     if entity == Entity.SYMBOL:
#     #         query = queries.SymbolQueries.LOAD_DACS
#     #         symbols: List = self._target.get_symbols(query=query, shard=self._shard)
#     #         dacs_rank: Dict[str, int] = {s[1]: s[0] for s in symbols}

#     #         for s in records["symbols"]:
#     #             s[BASE_ASSET_DACS_RANK] = dacs_rank.get(s[BASE_ASSET], None)
#     #             s[QUOTE_ASSET_DACS_RANK] = dacs_rank.get(s[QUOTE_ASSET], None)

#     #         return records["symbols"]

#     #     if entity == Entity.KLINE_1D:
#     #         return [
#     #             {
#     #                 SYMBOL: symbol,
#     #                 OPEN_TIME: r[0],
#     #                 OPEN: r[1],
#     #                 HIGH: r[2],
#     #                 LOW: r[3],
#     #                 CLOSE: r[4],
#     #                 VOLUME: r[5],
#     #                 CLOSE_TIME: r[6],
#     #                 QUOTE_ASSET_VOLUME: r[7],
#     #                 NUMBER_OF_TRADES: r[8],
#     #                 TAKER_BUY_BASE_ASSET_VOLUME: r[9],
#     #                 TAKER_BUY_QUOTE_ASSET_VOLUME: r[10],
#     #                 IGNORED: r[11],
#     #             }
#     #             for r in records
#     #         ]

#     #     return []

#     # def process(
#     #     self, delivery_id: int, entity: Entity, records: List[Record]
#     # ) -> Events:
#     #     """Processes entity records present in delivery.

#     #     Args:
#     #         delivery_id: Delivery id.
#     #         entity: Entity type.
#     #         records: Entity records.

#     #     Returns:
#     #         A dictionary with EventType (CREATE, AMEND, REMOVE) as key and a list
#     #         containing the event logs for each event type as value.
#     #     """
#     #     logger.info(f"Delivery {delivery_id}: processing {entity}...")

#     #     query: BaseQueries = self._queries[entity]
#     #     state_type: Type[State] = self._state[entity]

#     #     # previous state
#     #     keys: Keys = state_type.list_ids_from_source(records=records)
#     #     # fetch records from state with keys
#     #     prev_state: List[Tuple] = self._target.get_current_state(
#     #         query=query.LOAD_STATE, args=keys
#     #     )
#     #     prev_records: Dict[Key, State] = {}
#     #     for record in prev_state:
#     #         state = state_type.from_target(record=record)
#     #         prev_records[state.key] = state

#     #     # current state
#     #     curr_records: List[State] = [
#     #         state_type.from_source(record=record) for record in records
#     #     ]

#     #     del records

#     #     # compute events
#     #     events: Events = self.compute_events(
#     #         delivery_id=delivery_id,
#     #         entity=entity,
#     #         curr=curr_records,
#     #         prev=prev_records,
#     #     )

#     #     return events

#     # def compute_events(
#     #     self,
#     #     delivery_id: int,
#     #     entity: Entity,
#     #     curr: List[State],
#     #     prev: Dict[Key, State],
#     # ) -> Events:
#     #     """Computes change events between current state and delivery file records.

#     #     Args:
#     #         delivery_id: Delivery id.
#     #         entity: Entity.
#     #         curr: Entity records in delivery.
#     #         prev: Entity records in system.

#     #     Returns:
#     #         A dictionary with EventType (CREATE, AMEND, REMOVE) as key and a list
#     #         containing the event logs for each event type as value.
#     #     """
#     #     state_type: Type[State] = self._state[entity]
#     #     event_log_type: Type[EventLog] = self._event_log[entity]

#     #     # events
#     #     create: List[EventLog] = []
#     #     amend: List[EventLog] = []
#     #     remove: List[EventLog] = []

#     #     # in memory delivery variables
#     #     # needed to compute events faster
#     #     events: Dict[Key, State] = prev

#     #     it_event_id = self._target.get_next_event_id(n=len(curr))

#     #     for i, item in enumerate(curr):
#     #         if i % 100_000 == 0:
#     #             logger.info(
#     #                 f"Delivery {delivery_id}: {entity} processed {i}/{len(curr)}..."
#     #             )

#     #         # in case multiple actions for same primary key exist in same delivery
#     #         if item.key in events.keys():
#     #             # get latest update to compare state
#     #             prev_item = self.find(needle=item.key, haystack=events)

#     #             # if last update is equal to current version to update just jump
#     #             if prev_item is not None and item.hash == prev_item.hash:
#     #                 continue

#     #             # assign delivery_id to current state
#     #             item.delivery_id = delivery_id
#     #             # assign event_id to current_state
#     #             item.event_id = next(it_event_id)

#     #             event_log = event_log_type.from_states(
#     #                 event_type=EventType.AMEND, curr=item, prev=prev_item
#     #             )
#     #             amend.append(event_log)
#     #             events[item.key] = item
#     #             continue

#     #         if item.key not in events.keys():
#     #             # assign delivery_id to current state
#     #             item.delivery_id = delivery_id
#     #             # assign event_id to current_state
#     #             item.event_id = next(it_event_id)

#     #             event_log = event_log_type.from_states(
#     #                 event_type=EventType.CREATE, curr=item, prev=None
#     #             )
#     #             create.append(event_log)
#     #             events[item.key] = item
#     #             continue

#     #     prev_keys: Set[Key] = set(events.keys()) - set(item.key for item in curr)
#     #     it_event_id = self._target.get_next_event_id(n=len(prev_keys))

#     #     for prev_key in prev_keys:
#     #         # if prev_item.key not in curr_keys:
#     #         item = state_type.removal_instance(
#     #             event_id=next(it_event_id),
#     #             delivery_id=delivery_id,
#     #             key=prev_key,
#     #         )
#     #         prev_item = self.find(needle=prev_key, haystack=events)
#     #         event_log = event_log_type.from_states(
#     #             event_type=EventType.REMOVE, curr=item, prev=prev_item
#     #         )
#     #         remove.append(event_log)

#     #     del it_event_id

#     #     return {
#     #         EventType.CREATE: create,
#     #         EventType.AMEND: amend,
#     #         EventType.REMOVE: remove,
#     #     }

#     # @staticmethod
#     # def find(needle: Key, haystack: Dict[Key, State]) -> State:
#     #     """Given a needle searches the haystack and returns the match.

#     #     Args:
#     #         needle: key of entity to look for.
#     #         haystack: list of objects where to look for.

#     #     Returns:
#     #         Matching object if one exists.
#     #     """
#     #     return haystack[needle]

#     # @staticmethod
#     # def summarizer(delivery: Delivery) -> Summary:
#     #     """Makes statistical summary of events per entity within a delivery.

#     #     Args:
#     #         delivery: A dictionary with Entity as key and another dictionary
#     #             with Events as value.
#     #             Each Event dictionary is composed by EventType (CREATE, AMEND,
#     #             REMOVE) as key and a list containing the event logs for each
#     #             event type as value.

#     #     Returns:
#     #         A summary, with the same structure as the input but instead of
#     #         having a list structure with events, is the length of the list.
#     #     """
#     #     summary = {}
#     #     for entity, events in delivery.items():
#     #         event_cnt = {}
#     #         for event_type, event_logs in events.items():
#     #             if event_logs:
#     #                 event_cnt[event_type] = len(event_logs)

#     #         if event_cnt:
#     #             summary[entity] = event_cnt

#     #     return summary

#     # def persist_delivery(
#     #     self,
#     #     delivery_id: int,
#     #     entity: Entity,
#     #     start_time: datetime,
#     #     delivery: Delivery,
#     # ) -> None:
#     #     """Persists records present in delivery.

#     #     Args:
#     #         delivery_id: Delivery id.
#     #         entity: entity processed in delivery.
#     #         start_time: Time delivery started.
#     #         delivery: Delivery to process.
#     #     """
#     #     self._target.begin_transaction()

#     #     for entity, events in delivery.items():
#     #         self.persist_postgres(entity=entity, events=events)

#     #         logger.info(
#     #             f"Delivery {delivery_id}: {entity} ("
#     #             f"create: {len(events[EventType.CREATE])}, "
#     #             f"amend: {len(events[EventType.AMEND])}, "
#     #             f"remove: {len(events[EventType.REMOVE])})."
#     #         )

#     #     summary = self.summarizer(delivery=delivery)
#     #     end_time: datetime = datetime.utcnow()
#     #     self._target.persist_delivery(
#     #         args={
#     #             "delivery_id": delivery_id,
#     #             "entity": entity,
#     #             "shard": self._shard,
#     #             "row_creation": datetime.utcnow(),
#     #             "summary": json.dumps(summary, cls=MessagesEncoder),
#     #             "runtime": end_time - start_time,
#     #         }
#     #     )

#     #     self._target.commit_transaction()
#     #     logger.info(f"Delivery {delivery_id}: persisted to postgres.")

#     #     logger.info(f"Delivery {delivery_id}: persisted {summary}.")

#     # def persist_postgres(self, entity: Entity, events: Events) -> None:
#     #     """Persists records of entity to postgres.

#     #     Args:
#     #         entity: Entity which events are going to be persisted.
#     #         events: Events (CREATE, AMEND, REMOVE) to persist.
#     #     """
#     #     query: BaseQueries = self._queries[entity]

#     #     # if multiple instructions have the same primary key
#     #     # db instructions can't be in batch
#     #     batch_create = len(set(e.curr.key for e in events[EventType.CREATE])) == len(  # noqa: B950
#     #         events[EventType.CREATE]
#     #     )
#     #     batch_amend = len(set(e.curr.key for e in events[EventType.AMEND])) == len(
#     #         events[EventType.AMEND]
#     #     )

#     #     # CREATE
#     #     self._target.execute(
#     #         instruction=query.APPEND_LOG,
#     #         logs=[e.as_record() for e in events[EventType.CREATE]],
#     #     )
#     #     if batch_create:
#     #         self._target.execute(
#     #             instruction=query.UPSERT,
#     #             logs=[e.curr.as_tuple() for e in events[EventType.CREATE]],
#     #         )
#     #     else:
#     #         for e in events[EventType.CREATE]:
#     #             self._target.execute(
#     #                 instruction=query.UPSERT,
#     #                 logs=[e.curr.as_tuple()],
#     #             )

#     #     # AMEND
#     #     self._target.execute(
#     #         instruction=query.APPEND_LOG,
#     #         logs=[e.as_record() for e in events[EventType.AMEND]],
#     #     )
#     #     if batch_amend:
#     #         self._target.execute(
#     #             instruction=query.UPSERT,
#     #             logs=[e.curr.as_tuple() for e in events[EventType.AMEND]],
#     #         )
#     #     else:
#     #         for e in events[EventType.AMEND]:
#     #             self._target.execute(
#     #                 instruction=query.UPSERT,
#     #                 logs=[e.curr.as_tuple()],
#     #             )

#     #     # REMOVE
#     #     self._target.execute(
#     #         instruction=query.APPEND_LOG,
#     #         logs=[e.as_record() for e in events[EventType.REMOVE]],
#     #     )
#     #     self._target.execute(
#     #         instruction=query.DELETE,
#     #         logs=[e.curr.key for e in events[EventType.REMOVE]],
#     #     )

#     # def publish_messages(self, delivery_id: int, delivery: Delivery) -> None:
#     #     """Publishes messages.

#     #     Args:
#     #         delivery_id: Delivery id.
#     #         delivery: Delivery to publish.
#     #     """
#     #     self._notifier.keep_alive()

#     #     max_event_id: Optional[int] = None
#     #     for _, events in delivery.items():
#     #         for _, event_logs in events.items():
#     #             for log in event_logs:
#     #                 self._notifier.notify_event(event=log)
#     #                 event_id = log.curr.event_id
#     #                 assert event_id is not None
#     #                 max_event_id = (
#     #                     event_id
#     #                     if max_event_id is None or event_id >= max_event_id
#     #                     else max_event_id
#     #                 )

#     #     summary = self.summarizer(delivery=delivery)
#     #     self._notifier.notify_datasource_update(
#     #         summary=summary,
#     #         event_id=max_event_id,
#     #     )

#     #     logger.info(f"Delivery {delivery_id}: messages published.")

#     # def declare_metrics(self) -> None:
#     #     """Initializes all prometheus metrics."""
#     #     container_age = Gauge(
#     #         "container_age", " Start time of the process since unix epoch in seconds."  # noqa: B950
#     #     )
#     #     container_age.set(datetime.utcnow().timestamp())
#     #     self._last_delivery = Gauge(
#     #         "last_delivery",
#     #         "Time of last file/batch process since unix epoch in seconds.",
#     #     )
#     #     self._last_delivery.set(datetime.utcnow().timestamp())

#     #     for value in self._entities:
#     #         counter = Counter(
#     #             value,
#     #             f"Number of {value} records.",
#     #             ["name", "version", "unit", "component", "operation"],
#     #         )
#     #         for op in ["create", "amend", "remove"]:
#     #             counter.labels(
#     #                 "binance-delivery-api", __version__, "analytics", "loaders", op  # noqa: B950
#     #             )
#     #         self._counters[value] = counter

#     #         counter = Counter(
#     #             f"{value}_status_code",
#     #             f"Number of {value} records.",
#     #             ["name", "version", "unit", "component", "operation"],
#     #         )
#     #         for code in self._status_codes.keys():
#     #             counter.labels(
#     #                 "binance-delivery-api", __version__, "analytics", "loaders", code  # noqa: B950
#     #             )

#     #         self._counters_status_code[value] = counter

#     # def increment_counters(self, delivery_id: int, delivery: Delivery) -> None:
#     #     """Increments prometheus counters.

#     #     Args:
#     #         delivery_id: Delivery id.
#     #         delivery: Delivery to increment prometheus counters.
#     #     """
#     #     for entity, events in delivery.items():
#     #         counter = self._counters[entity]
#     #         counter.labels(
#     #             "binance-delivery-api", __version__, "analytics", "loaders", "create"  # noqa: B950
#     #         ).inc(amount=len(events[EventType.CREATE]))
#     #         counter.labels(
#     #             "binance-delivery-api", __version__, "analytics", "loaders", "amend"  # noqa: B950
#     #         ).inc(amount=len(events[EventType.AMEND]))
#     #         counter.labels(
#     #             "binance-delivery-api", __version__, "analytics", "loaders", "remove"  # noqa: B950
#     #         ).inc(amount=len(events[EventType.REMOVE]))

#     #     self._last_delivery.set(datetime.utcnow().timestamp())

#     #     logger.info(f"Delivery {delivery_id}: prometheus counters incremented.")

#     # def increment_status_code(self, entity: Entity, status_code: int) -> None:
#     #     """Increments prometheus counters.

#     #     Args:
#     #         entity: Entity scraped.
#     #         status_code: Status code of response scraped.
#     #     """
#     #     counter = self._counters_status_code[entity]
#     #     counter.labels(
#     #         "binance-delivery-api", __version__, "analytics", "loaders", status_code
#     #     ).inc(amount=1)

#     #     logger.info(f"Entity {entity}: prometheus status code counters incremented.")  # noqa: B950
