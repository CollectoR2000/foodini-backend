from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from core import crypto
from database.mappings import CreateUserV1, StoredUserV1, UpdateUserV1
from database.models import User

from .base import CRUD


class UserCRUD(CRUD[User, CreateUserV1, UpdateUserV1]):
    def create(self, db: Session, data: Union[CreateUserV1, Dict[str, Any]], *, commit: bool = True, **properties) -> User:
        if not isinstance(data, dict):
            data = data.dict()
        password = data.pop("password")
        data["hashed_password"] = crypto.hash_password(password)
        model = self.model(**data, **properties)
        db.add(model)
        if commit:
            db.commit()
        return model

    def read_username(self, db: Session, username: str) -> StoredUserV1:
        return db.query(self.model).filter(self.model.username.ilike(username)).first()


user = UserCRUD(User, StoredUserV1)
