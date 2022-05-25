from sqlalchemy import Boolean, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import CreatedColumn, DefaultString, Model, NotNullColumn, UpdatedColumn


class Ingredient(Model):
    recipe_id = NotNullColumn(Integer, ForeignKey("recipe.id", ondelete="CASCADE"))
    recipe = relationship("Recipe", back_populates="ingredients")
    name = NotNullColumn(DefaultString)
    optional = NotNullColumn(Boolean, default=False)
    comment = Column(DefaultString)
    user_id = NotNullColumn(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="ingredients")
    created_at = CreatedColumn()
    updated_at = UpdatedColumn()
    __table_args__ = (UniqueConstraint("recipe_id", "name"), )
