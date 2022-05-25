from datetime import datetime

from pydantic import constr

from .base import Mapping, ORMMapping, default_str


class CreateUserV1(Mapping):
    username: default_str
    first_name: default_str
    last_name: default_str
    password: default_str


class UpdateUserV1(Mapping):
    username: default_str | None = None
    first_name: default_str | None = None
    last_name: default_str | None = None
    password: default_str | None = None


class StoredUserV1(ORMMapping):
    id: int
    username: default_str
    first_name: default_str
    last_name: default_str
    admin: bool
    active: bool
    created_at: datetime
    updated_at: datetime


class HiddenUserV1(StoredUserV1):
    hashed_password: constr(min_length=60, max_length=60)
