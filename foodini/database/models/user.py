from sqlalchemy import CHAR, Boolean
from sqlalchemy.orm import relationship

from .base import CreatedColumn, DefaultString, Model, NotNullColumn, UpdatedColumn


class User(Model):
    username = NotNullColumn(DefaultString, unique=True)
    first_name = NotNullColumn(DefaultString)
    last_name = NotNullColumn(DefaultString)
    admin = NotNullColumn(Boolean, default=False)
    active = NotNullColumn(Boolean, default=False)
    hashed_password = NotNullColumn(CHAR(60))
    created_at = CreatedColumn()
    updated_at = UpdatedColumn()
    recipes = relationship("Recipe", back_populates="user", cascade="all, delete", passive_deletes=True)
    ingredients = relationship("Ingredient", back_populates="user", cascade="all, delete", passive_deletes=True)
