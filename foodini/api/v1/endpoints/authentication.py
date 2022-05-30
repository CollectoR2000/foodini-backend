from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import deps, security
from core import crypto, settings
from database import crud, mappings, models

router = APIRouter()


@router.post("/authentication/login", response_model=mappings.StoredUserV1)
def login(
    *,
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(deps.database),
    response: Response
) -> models.User:
    user: models.User = crud.user.read_username(db, credentials.username)
    if not user:
        raise HTTPException(status_code=401)
    if not crypto.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401)
    if not user.active:
        raise HTTPException(status_code=401)
    access_token = crypto.create_access_token(data={"username": user.username})
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}",
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True, secure=True, samesite="strict"
    )
    return user


@router.delete("/authentication/logout", status_code=204)
def logout(
    *,
    _: mappings.StoredUserV1 = Depends(security.authenticated)
) -> mappings.StoredUserV1:
    response = Response()
    response.delete_cookie(key="access_token")
    return response


@router.get("/authentication/whoami", response_model=mappings.StoredUserV1)
def whoami(
    *,
    user: mappings.StoredUserV1 = Depends(security.authenticated)
) -> mappings.StoredUserV1:
    return user
