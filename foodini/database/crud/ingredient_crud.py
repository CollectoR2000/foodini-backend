from sqlalchemy.orm import Session

from database.mappings import CreateIngredientV1, StoredIngredientV1, UpdateIngredientV1
from database.models import Ingredient

from .base import CRUD


class IngredientCRUD(CRUD[Ingredient, CreateIngredientV1, UpdateIngredientV1]):
    def read_name(self, db: Session, name: str) -> StoredIngredientV1:
        return db.query(self.model).filter(self.model.name == name).first()


ingredient = IngredientCRUD(Ingredient, StoredIngredientV1)
