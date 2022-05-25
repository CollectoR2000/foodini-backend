from datetime import datetime
from typing import List

from .base import Mapping, ORMMapping, default_str
from .ingredient import CreateIngredientV1, StoredIngredientV1


class CreateRecipeV1(Mapping):
    name: default_str
    method_of_preperation: str
    ingredients: List[CreateIngredientV1] = []


class UpdateRecipeV1(Mapping):
    name: default_str | None = None
    method_of_preperation: str | None = None
    published: bool | None = None


class StoredRecipeV1(ORMMapping):
    id: int
    name: default_str
    method_of_preperation: str
    published: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
    ingredients: List[StoredIngredientV1]
