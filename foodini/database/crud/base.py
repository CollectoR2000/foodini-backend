from typing import Any, Dict, Generic, List, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.orm import Session

from core import settings
from database import Order
from database.models.base import Model

ModelGeneric = TypeVar("ModelGeneric", bound=Model)
MappingGeneric = TypeVar("MappingGeneric", bound=BaseModel)
CreateGeneric = TypeVar("CreateGeneric", bound=BaseModel)
UpdateGeneric = TypeVar("UpdateGeneric", bound=BaseModel)


class CRUD(Generic[ModelGeneric, CreateGeneric, UpdateGeneric]):
    def __init__(self, model: ModelGeneric, mapping: MappingGeneric) -> None:
        self.model = model
        self.mapping = mapping

    def order(self, order: Order):
        return self.model.id.desc() if order == order.desc else self.model.id.asc()

    def compile_filters(self) -> list:
        return []

    def count(self, db: Session, **filters) -> int:
        query = db.query(self.model)
        compiled_filters = self.compile_filters(**filters)
        if compiled_filters:
            query = query.filter(*compiled_filters)
        return query.count()

    def create(self, db: Session, data: Union[CreateGeneric, Dict[str, Any]], *, commit: bool = True, **properties) -> ModelGeneric:
        if not isinstance(data, dict):
            data = data.dict()
        model = self.model(**data, **properties)
        db.add(model)
        if commit:
            db.commit()
        return model

    def read(self, db: Session, id: int) -> ModelGeneric:
        return db.query(self.model).filter(self.model.id == id).first()

    def read_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = settings.DATABASE_LIMIT,
        order: Order = Order.asc,
        **filters
    ) -> List[ModelGeneric]:
        query = db.query(self.model).order_by(self.order(order))
        compiled_filters = self.compile_filters(**filters)
        if compiled_filters:
            query = query.filter(*compiled_filters)
        return query.offset(skip).limit(limit if limit else None).all()

    def update(self, db: Session, model: ModelGeneric, update: Union[UpdateGeneric, dict], *, commit: bool = True) -> ModelGeneric:
        current = self.mapping.from_orm(model).dict(exclude_unset=False)
        update = update.dict(exclude_unset=True) if not isinstance(update, dict) else update
        for key, value in update.items():
            if key in current:
                setattr(model, key, value)
            else:
                raise AttributeError(f"AttributeError, {model.__class__.__name__!r} doesn't have the column {key!r}.")
        db.add(model)
        if commit:
            db.commit()
        return model

    def delete(self, db: Session, model: Union[ModelGeneric, int], *, commit: bool = True) -> ModelGeneric:
        if isinstance(model, int):
            model = self.read(db, model)
        db.delete(model)
        if commit:
            db.commit()
        return None
