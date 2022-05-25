from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .base import CreatedColumn, DefaultString, Model, NotNullColumn, UpdatedColumn


class Recipe(Model):
    name = NotNullColumn(DefaultString, unique=True)
    method_of_preperation = NotNullColumn(Text)
    published = NotNullColumn(Boolean, default=False)
    user_id = NotNullColumn(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="recipes")
    created_at = CreatedColumn()
    updated_at = UpdatedColumn()
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete", passive_deletes=True)
