from sqlalchemy.orm import Session

from database.mappings import CreateUserV1, StoredUserV1, UpdateUserV1
from database.models import User

from .base import CRUD


class UserCRUD(CRUD[User, CreateUserV1, UpdateUserV1]):
    def read_username(self, db: Session, username: str) -> StoredUserV1:
        return db.query(self.model).filter(self.model.username.ilike(username)).first()


user = UserCRUD(User, StoredUserV1)
