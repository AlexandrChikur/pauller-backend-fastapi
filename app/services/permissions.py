from typing import Dict

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from app.api.dependencies.database import get_repository
from app.core import config
from app.db.repositories.users import UsersRepository
from app.resources import strings
from app.services.jwt import get_username_from_token


async def get_permissions(
    request: Request,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> Dict[str, bool]:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.AUTHENTICATION_REQUIRED,
        )
    user = await users_repo.get_user_by_username(
        username=get_username_from_token(
            token=auth_header.split()[-1], secret_key=str(config.SECRET_KEY)
        )
    )

    return {"is_active": user.is_active, "is_admin": user.is_admin}
