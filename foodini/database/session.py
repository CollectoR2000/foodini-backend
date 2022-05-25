from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import settings

from .models.base import Model

engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True, pool_recycle=3600, isolation_level="READ COMMITTED", pool_size=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


if settings.DATABASE_INIT:
    Model.metadata.create_all(bind=engine)
