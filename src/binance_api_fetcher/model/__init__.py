"""binance_api_fetcher data model."""

from .entity import Entity
from .service import Service, ServiceError

__all__ = [
    "Entity",
    "Service",
    "ServiceError",
]
