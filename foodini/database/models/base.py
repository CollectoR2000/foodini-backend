import re
from functools import partial

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func

NotNullColumn = partial(Column, nullable=False)
DefaultString: String = partial(String, length=256)()
CreatedColumn = partial(NotNullColumn, DateTime, server_default=func.now())
UpdatedColumn = partial(NotNullColumn, DateTime, server_default=func.now(), onupdate=func.now())


@as_declarative()
class Model:
    """
    Base class for alle SQLAlchemy tables with automatic primary key and tablename.
    """
    id: int = NotNullColumn(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Transform table name from CamelCase to snake_case.
        Example: 'ExampleTable' becomes 'example_table'.
        """
        tablename = cls.__name__
        tablename = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', tablename)
        tablename = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', tablename)
        tablename = tablename.replace("-", "_")
        return tablename.lower()
