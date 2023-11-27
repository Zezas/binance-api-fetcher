"""Loader execution class."""

import argparse
import ast
import logging
import os
from sys import stdout

# TODO maybe put the config inside a function
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s.%(msecs)06d %(levelname)s [%(filename)s:%(lineno)d] %(message)s",  # noqa: B950
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=stdout,
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parses user input arguments when starting loading process.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="python ./src/binance_api_fetcher/__main__.py"
    )

    # TODO maybe add a --log variable

    parser.add_argument(
        "--service",
        dest="run_as_service",
        action="store_true",
        required=False,
        help="Enable continuous pooling of source.",
    )
    parser.add_argument(
        "--no-service",
        dest="run_as_service",
        action="store_false",
        required=False,
        help="Disable continuous pooling of source.",
    )
    parser.set_defaults(
        run_as_service=ast.literal_eval(os.environ.get("RUN_AS_SERVICE", "True"))
    )

    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        required=False,
        help="Disable data persistence (parse only).",
    )
    parser.add_argument(
        "--no-dry-run",
        dest="dry_run",
        action="store_false",
        required=False,
        help="Enable data persistence (default).",
    )
    parser.set_defaults(dry_run=ast.literal_eval(os.environ.get("DRY_RUN", "False")))

    parser.add_argument(
        "--source",
        dest="source",
        type=str,
        required=False,
        default=os.environ.get("SOURCE"),
        help="Binance API url. e.g.: https://api.binance.com/api/v3/",
    )

    parser.add_argument(
        "--target",
        dest="target",
        type=str,
        required=False,
        default=os.environ.get("TARGET"),
        help="Postgres connection URL. e.g.: "
        "user=username password=password host=localhost port=5432 dbname=binance",
    )

    parser.add_argument(
        "--min_sleep",
        dest="min_sleep",
        default=int(os.getenv("MIN_SLEEP", default=15)),
        type=int,
        required=False,
        help="Service minimum time to sleep between iterations.",
    )

    parser.add_argument(
        "--max_sleep",
        dest="max_sleep",
        default=int(os.getenv("MAX_SLEEP", default=30)),
        type=int,
        required=False,
        help="Service maximum time to sleep between iterations.",
    )

    parser.add_argument(
        "--scrape-symbol",
        dest="symbol",
        action="store_true",
        required=False,
        help="Enable symbol scraping.",
    )
    parser.add_argument(
        "--no-scrape-symbol",
        dest="symbol",
        action="store_false",
        required=False,
        help="Disable symbol scraping.",
    )
    parser.set_defaults(symbol=ast.literal_eval(os.environ.get("SYMBOL", "False")))

    parser.add_argument(
        "--scrape-kline-1d",
        dest="kline_1d",
        action="store_true",
        required=False,
        help="Enable kline_1d scraping.",
    )
    parser.add_argument(
        "--no-scrape-kline-1d",
        dest="kline_1d",
        action="store_false",
        required=False,
        help="Disable kline_1d scraping.",
    )
    parser.set_defaults(kline_1d=ast.literal_eval(os.environ.get("KLINE_1D", "False")))

    parser.add_argument(
        "--datapoint-limit",
        dest="datapoint_limit",
        default=int(os.getenv("DATAPOINT_LIMIT", default=500)),
        type=int,
        required=False,
        help="Service datapoint limit.",
    )

    parser.add_argument(
        "--shard",
        dest="shard",
        default=int(os.getenv("SHARD", default=0)),
        type=int,
        required=False,
        help="Service shard.",
    )

    args_parsed: argparse.Namespace = parser.parse_args()

    return args_parsed


def main() -> None:
    """Run the binance_api_fetcher service.

    Get arguments, create service instance and run service.
    """
    # Startup message
    logger.info("Starting service...")
    # Get args
    parsed_args: argparse.Namespace = parse_args()
    logger.debug(parsed_args)
    # TODO service instance receives arguments
    # Create service instance
    # service: Service = Service(args=parsed_args)
    # TODO service instance runs without argumetns
    # Run service
    # service.run()


if __name__ == "__main__":  # pragma: no cover
    main()
