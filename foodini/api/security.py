from datetime import datetime

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from api import deps
from core import OAuth2PasswordCookieBearer, settings
from database import crud, mappings, models

oauth2_scheme = OAuth2PasswordCookieBearer(token_url=f"{settings.API_ENDPOINT_PREFIX}{settings.API_V1_PREFIX}/authentication/token")


def authenticated(db: Session = Depends(deps.database), token: str = Depends(oauth2_scheme)) -> mappings.StoredUserV1:
    exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SIGNING_ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    if datetime.fromtimestamp(payload["exp"]) < datetime.now():
        raise exception
    user: models.User = crud.user.read_username(db, username)
    if not user:
        raise exception
    if not user.active:
        raise exception
    return mappings.StoredUserV1.from_orm(user)


def authorised(user: mappings.StoredUserV1 = Depends(authenticated)) -> mappings.StoredUserV1:
    if not user.admin:
        raise HTTPException(status_code=403)
    return user
