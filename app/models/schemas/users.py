from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from app.models.common import IDModelMixin
from app.services import security


class User(BaseModel):
    username: str
    email: Optional[EmailStr]
    bio: Optional[str] = ""
    image: Optional[str] = None


class UserWithStates(User):
    is_active: bool = False
    is_admin: bool = False


class UserInLogin(BaseModel):
    email_or_login: str
    password: str


class UserInCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserWithToken(User):
    token: str


class UserInResponse(BaseModel):
    user: UserWithToken


class UserInUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    bio: Optional[str] = ""
    image: Optional[HttpUrl] = None


class UserInDB(IDModelMixin, UserWithStates):
    # salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(password, self.hashed_password)

    def change_password(self, password: str) -> None:
        # self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(password)
