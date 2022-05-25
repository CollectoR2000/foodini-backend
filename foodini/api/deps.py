from typing import Generator

from database import SessionLocal


def database() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
