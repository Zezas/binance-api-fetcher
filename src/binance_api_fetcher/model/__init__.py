"""binance_api_fetcher data model."""

from .entity import Entity
from .service import Service, ServiceError
from .status_code import StatusCode

__all__ = [
    "Entity",
    "Service",
    "ServiceError",
    "StatusCode",
]
