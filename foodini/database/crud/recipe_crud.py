from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database.mappings import CreateRecipeV1, StoredRecipeV1, UpdateRecipeV1
from database.models import Recipe

from .base import CRUD


class RecipeCRUD(CRUD[Recipe, CreateRecipeV1, UpdateRecipeV1]):
    def compile_filters(self, *, user_id: int | None = None, published: bool | None = None) -> list:
        filters = []
        if user_id:
            filters.append(self.model.user_id == user_id)
        if published is not None:
            filters.append(self.model.published == published)
        return filters

    def read_name(self, db: Session, name: str) -> StoredRecipeV1:
        return db.query(self.model).filter(self.model.name == name).first()

    def read_random(self, db: Session, **filters) -> StoredRecipeV1:
        query = db.query(self.model)
        compiled_filters = self.compile_filters(**filters)
        if compiled_filters:
            query = query.filter(*compiled_filters)
        return query.order_by(func.random()).first()


recipe = RecipeCRUD(Recipe, StoredRecipeV1)
