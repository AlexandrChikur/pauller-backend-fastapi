from typing import Optional

from app.db.errors.common import EntityDoesNotExistError
from app.db.queries.users import (
    CREATE_USER_QUERY,
    GET_USER_BY_EMAIL,
    GET_USER_BY_USERNAME,
    UPDATE_USER,
)
from app.db.repositories.base import BaseRepository
from app.models.schemas.users import UserInDB


class UsersRepository(BaseRepository):
    async def create_user(
        self, *, username: str, email: str, password: str,
    ) -> UserInDB:
        user = UserInDB(
            username=username, email=email, password=password, is_active=True
        )
        user.change_password(password)
        await self._conn.execute(
            CREATE_USER_QUERY,
            user.username,
            user.email,
            user.hashed_password,
            user.bio,
            user.image,
            user.is_active,
            user.is_super,
            user.is_staff,
        )

        return user

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_row = await self._conn.fetchrow(GET_USER_BY_USERNAME, username)

        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExistError(f"entity with username {username} does not exist")

    async def get_user_by_email(self, *, email: str) -> UserInDB:
        user_row = await self._conn.fetchrow(GET_USER_BY_EMAIL, email)

        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExistError(f"entity with email {email} does not exist")

    async def update_user(
        self,
        *,
        user: UserInDB,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        bio: Optional[str] = None,
        image: Optional[str] = None,
    ) -> UserInDB:
        user_in_db = await self.get_user_by_username(username=user.username)

        user_in_db.username = username or user_in_db.username
        user_in_db.email = email or user_in_db.email
        user_in_db.bio = bio or user_in_db.bio
        user_in_db.image = image or user_in_db.image
        if password:
            user_in_db.change_password(password)

        await self._conn.execute(
            UPDATE_USER,
            user.username,
            user_in_db.username,
            user_in_db.email,
            user_in_db.hashed_password,
            user_in_db.bio,
            user_in_db.image,
        )

        return user_in_db
