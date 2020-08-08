from typing import Optional

from fastapi import Depends, HTTPException, status

from app.api.dependencies.database import get_repository
from app.core.config import SECRET_KEY
from app.db.errors.users import EntityDoesNotExistError
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import UserInDB
from app.resources import strings
from app.services.jwt import get_username_from_token


async def get_current_user(
    token: str, users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> UserInDB:
    username = get_username_from_token(token, str(SECRET_KEY))
    try:
        user = await users_repo.get_user_by_username(username=username)
    except EntityDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.TOKEN_NOT_VALID
        )

    return user
