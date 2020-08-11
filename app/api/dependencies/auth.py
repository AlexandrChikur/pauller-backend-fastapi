from typing import Callable, Optional

from fastapi import Depends, HTTPException, Security, requests, status
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.dependencies.database import get_repository
from app.core.config import JWT_TOKEN_PREFIX, SECRET_KEY
from app.db.errors.common import EntityDoesNotExistError
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import UserInDB
from app.resources import strings
from app.services import jwt

HEADER_KEY = "Authorization"


class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: requests.Request,) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as err:
            raise HTTPException(
                status_code=err.status_code, detail=strings.AUTHENTICATION_REQUIRED
            )


def get_current_user_authorizer(*, required: bool = True) -> Callable:
    return _get_current_user if required else _get_current_user_optional


def _get_authorization_header_retriever(*, required: bool = True,) -> Callable:
    return _get_authorization_header if required else _get_authorization_header_optional


def _get_authorization_header(
    api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.WRONG_TOKEN_PREFIX,
        )

    if token_prefix != JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.WRONG_TOKEN_PREFIX,
        )

    return token


def _get_authorization_header_optional(
    authorization: Optional[str] = Security(
        RWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
    ),
) -> str:
    if authorization:
        return _get_authorization_header(authorization)

    return ""


async def _get_current_user(
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token: str = Depends(_get_authorization_header_retriever()),
) -> UserInDB:
    try:
        username = jwt.get_username_from_token(token, str(SECRET_KEY))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.MALFORMED_PAYLOAD,
        )

    try:
        return await users_repo.get_user_by_username(username=username)
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.MALFORMED_PAYLOAD,
        )


async def _get_current_user_optional(
    repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token: str = Depends(_get_authorization_header_retriever(required=False)),
) -> Optional[UserInDB]:
    if token:
        return await _get_current_user(repo, token)

    return None
