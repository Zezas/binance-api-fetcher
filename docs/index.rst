The Binance API Fetcher Project
==============================

Insert short description that should be in the README.md also.

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference


Introduction
------------

Insert short description that should be in the README.md also.


Installation
------------

To install the Binance API Fetcher project,
run this command in your terminal:

.. code-block:: console

   $ pip install binance-api-fetcher


Usage
-----

Binance API Fetcher's usage looks like:

.. code-block:: console

   $ binance-api-fetcher [OPTIONS]

.. option:: --service, --no-service, RUN_AS_SERVICE=<True/False>

   Enable/Disable continuous pooling of source.
   Default is set to True.

.. option:: --dry-run, --no-dry-run, DRY_RUN=<True/False>

   Enable/Disable data persistance.
   Default is set to False.

.. option:: --source, SOURCE=<API URL>

   Binance API url. e.g.: "https://api.binance.com/api/v3/".

.. option:: --target, TARGET=<Database Connection>

   Postgres connection URL. e.g.:
   "user=username password=password host=localhost port=5432 dbname=binance".

.. option:: --min_sleep, MIN_SLEEP=<Seconds>

   Service minimum time to sleep between iterations.

.. option:: --max_sleep, MAX_SLEEP=<Seconds>

   Service maximum time to sleep between iterations.

.. option:: --scrape-symbol, --no-scrape-symbol, SYMBOL=<True/False>

   Enable/Disable symbol scraping.
   Default is set to False.

.. option:: --scrape-kline-1d, --no-scrape-kline-1d, KLINE_1D=<True/False>

   Enable/Disable kline_1d scraping.
   Default is set to False.

.. option:: --datapoint-limit, DATAPOINT_LIMIT=<Integer>

   Service datapoint limit.

.. option:: --shard, SHARD=<Integer>

   Service shard.

.. option:: --version

   Display the version and exit.

.. option:: --help

   Display a short usage message and exit.
