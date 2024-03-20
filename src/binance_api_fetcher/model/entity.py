"""Entity data model."""

from enum import Enum


class Entity(str, Enum):
    """Enum class that represents the entities created by the service."""

    KLINE_1D = "kline_1d"

    def __repr__(self) -> str:
        return str(self.value)
