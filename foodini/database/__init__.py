from enum import Enum

from .session import SessionLocal  # noqa: F401


class Order(Enum):
    asc: str = "asc"
    desc: str = "desc"
