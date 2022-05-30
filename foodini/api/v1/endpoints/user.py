from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from api import deps, security
from core import settings
from database import crud, mappings, models

router = APIRouter()


@router.post("/user", response_model=mappings.StoredUserV1, status_code=201)
def create_user(
    *,
    payload: mappings.CreateUserV1,
    db: Session = Depends(deps.database)
) -> models.User:
    if crud.user.read_username(db, payload.username):
        raise HTTPException(status_code=409)
    user: models.User = crud.user.create(db, payload, commit=True)
    return user


@router.get("/users", response_model=List[mappings.StoredUserV1], status_code=201)
def read_users(
    *,
    skip: int = 0,
    limit: int = settings.DATABASE_LIMIT,
    _: mappings.StoredUserV1 = Depends(security.authorised),
    db: Session = Depends(deps.database),
    response: Response
) -> List[models.User]:
    response.headers["Total-Count"] = str(crud.user.count(db))
    return crud.user.read_multi(db, skip=skip, limit=limit)


@router.get("/user/{id:int}", response_model=mappings.StoredUserV1)
def read_user(
    *,
    id: int,
    auth: mappings.StoredUserV1 = Depends(security.authenticated),
    db: Session = Depends(deps.database)
) -> models.User:
    user: models.User = crud.user.read(db, id)
    if not user:
        raise HTTPException(status_code=404)
    if not auth.admin and auth.id != user.id:
        raise HTTPException(status_code=403)
    return user


@router.patch("/user/{id:int}", response_model=mappings.StoredUserV1)
def update_user(
    *,
    id: int,
    payload: mappings.UpdateUserV1,
    auth: mappings.StoredUserV1 = Depends(security.authenticated),
    db: Session = Depends(deps.database)
) -> models.User:
    user: models.User = crud.user.read(db, id)
    if not user:
        raise HTTPException(status_code=404)
    if not auth.admin and auth.id != user.id:
        raise HTTPException(status_code=403)
    if not auth.admin and payload.active:
        raise HTTPException(status_code=403)
    if not auth.admin and payload.admin:
        raise HTTPException(status_code=403)
    user: models.User = crud.user.update(db, user, payload)
    return user


@router.delete("/user/{id:int}", status_code=204)
def delete_user(
    *,
    id: int,
    auth: mappings.StoredUserV1 = Depends(security.authenticated),
    db: Session = Depends(deps.database)
) -> None:
    user: models.User = crud.user.read(db, id)
    if not user:
        raise HTTPException(status_code=404)
    if not auth.admin and auth.id != auth:
        raise HTTPException(status_code=403)
    user: models.User = crud.user.delete(db, user)
    return None
