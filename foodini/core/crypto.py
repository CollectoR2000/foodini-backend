from datetime import datetime, timedelta
from typing import Dict

from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from passlib.context import CryptContext

from core import settings

crypt_context = CryptContext(schemes=[settings.HASHING_ALGORITHM], deprecated="auto")


class OAuth2PasswordCookieBearer(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str | None = None,
        scopes: Dict[str, str] | None = None,
        auto_error: bool = True
    ) -> None:
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)
        return None

    async def __call__(self, request: Request) -> str | None:
        authorization: str = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


def hash_password(password: str) -> str:
    return crypt_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return crypt_context.verify(password, hashed_password)


def create_access_token(data: dict):
    expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expires})
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.SIGNING_ALGORITHM)
    return encoded_jwt
