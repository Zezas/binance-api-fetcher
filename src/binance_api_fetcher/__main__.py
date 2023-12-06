"""Binance API Fetcher main file."""

import argparse
import ast
import logging
from logging import Logger
import os
from sys import stdout

from binance_api_fetcher.model import Service

logger: Logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parses user input arguments when starting the service.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="python ./src/binance_api_fetcher/__main__.py"
    )

    parser.add_argument(
        "--log-level",
        dest="log_level",
        type=str,
        required=False,
        default=os.environ.get("LOG_LEVEL", default="info"),
        help="Set the logging level (default: info).",
    )

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
        run_as_service=ast.literal_eval(
            os.environ.get("RUN_AS_SERVICE", default="True")
        )
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
    parser.set_defaults(
        dry_run=ast.literal_eval(os.environ.get("DRY_RUN", default="False"))
    )

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
        type=int,
        required=False,
        default=int(os.getenv("MIN_SLEEP", default=15)),
        help="Service minimum time to sleep between iterations (default: 15).",
    )

    parser.add_argument(
        "--max_sleep",
        dest="max_sleep",
        type=int,
        required=False,
        default=int(os.getenv("MAX_SLEEP", default=30)),
        help="Service maximum time to sleep between iterations (default: 30).",
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
    parser.set_defaults(
        symbol=ast.literal_eval(os.environ.get("SYMBOL", default="False"))
    )

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
    parser.set_defaults(
        kline_1d=ast.literal_eval(os.environ.get("KLINE_1D", default="False"))
    )

    parser.add_argument(
        "--datapoint-limit",
        dest="datapoint_limit",
        type=int,
        required=False,
        default=int(os.getenv("DATAPOINT_LIMIT", default=500)),
        help="Service datapoint limit (default: 500).",
    )

    parser.add_argument(
        "--shard",
        dest="shard",
        type=int,
        required=False,
        default=int(os.getenv("SHARD", default=0)),
        help="Service shard (default: 0).",
    )

    args_parsed: argparse.Namespace = parser.parse_args()

    return args_parsed


def logging_config(logging_level: str) -> None:
    """Configure the logging with the required level.

    Args:
        logging_level: The level of the logging.
    """
    logging.basicConfig(
        level=logging_level.upper(),
        format=(
            "%(asctime)s.%(msecs)06d %(levelname)s "
            "[%(filename)s:%(lineno)d] %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=stdout,
    )


def main() -> None:
    """Run the binance_api_fetcher service.

    Get arguments, configure logging,
    create service instance and run service.
    """
    # Get arguments
    parsed_args: argparse.Namespace = parse_args()
    # Configure logging
    logging_config(logging_level=parsed_args.log_level)
    logger.debug(msg=parsed_args)
    # Startup message
    logger.info(msg="Starting service...")
    # Create service instance
    service: Service = Service(args=parsed_args)
    logger.debug(msg=service)
    # TODO service instance runs without argumetns
    # Run service
    # service.run()


if __name__ == "__main__":  # pragma: no cover
    main()
