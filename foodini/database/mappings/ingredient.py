from datetime import datetime

from .base import Mapping, ORMMapping, default_str
from .user import StoredUserV1


class CreateIngredientV1(Mapping):
    name: default_str
    optional: bool = False
    comment: default_str | None = None


class UpdateIngredientV1(Mapping):
    name: default_str | None = None
    optional: bool | None = None
    comment: default_str | None = None


class StoredIngredientV1(ORMMapping):
    id: int
    recipe_id: int
    name: default_str
    optional: bool
    comment: str | None = None
    user_id: int
    user: StoredUserV1
    created_at: datetime
    updated_at: datetime
