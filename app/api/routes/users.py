from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException
from starlette import status

from app.api.dependencies.auth import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.core import config
from app.db.errors.common import EntityDoesNotExistError
from app.db.errors.users import WrongLoginError
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import (
    User,
    UserInCreate,
    UserInDB,
    UserInLogin,
    UserInResponse,
    UserInUpdate,
    UserWithStates,
    UserWithToken,
)
from app.resources import strings
from app.services import jwt
from app.services.auth import check_email_is_taken, check_username_is_taken
from app.api.dependencies.permissions import get_admin_permissionizer

router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInResponse,
    summary="Sign Up User",
    name="users:signup",
)
async def create_user(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    """
    Method for **create** user. <br/><br/>
    Allowed for ```any```. <br/>

    Request Body params (**all params required**): <br/>
    *::param::* username: str - The name of the user. <br/>
    *::param::* email: EmailStr - The email of the user, which **must match the email format**: _example@dom.ex_<br/>
    *::param::* password: str - The password of the user. <br/>
    """
    if await check_username_is_taken(users_repo, user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.USERNAME_TAKEN
        )

    if await check_email_is_taken(users_repo, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.EMAIL_TAKEN
        )

    user = await users_repo.create_user(**user_create.dict())
    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))

    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token,
        )
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserInResponse,
    summary="Log In User",
    name="users:login",
)
async def login_user(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    """
    Method for **login** user. <br/><br/>
    Allowed for ```any```. <br/>

    Request Body params (**all params required**): <br/>
    *::param::* login_or_email: str - The parameter that gives to user opportunity to login by username **or** email. <br/>
    *::param::* password: str - The password of the user.
    """
    try:
        user = await users_repo.get_user_by_username(username=user_login.email_or_login)
    except EntityDoesNotExistError:
        try:
            user = await users_repo.get_user_by_email(email=user_login.email_or_login)
        except EntityDoesNotExistError as existence_error:
            raise WrongLoginError from existence_error

    if not user.check_password(user_login.password):
        raise WrongLoginError

    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))

    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token,
        )
    )


@router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=UserInResponse,
    summary="Update User",
    name="users:update-current-user",
    dependencies=[Depends(get_admin_permissionizer())],
    tags=["admin"]
)
async def update_user(
    current_user: User = Depends(get_current_user_authorizer()),
    user_update: UserInUpdate = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:
    """
    Method for **update** user. <br/><br/>
    Allowed for ```admin``` only. <br/>

    The user who will be changed is determined by one of the parameters: *username* or *email*.
    If one parameter is found in the database and the second parameter differs from the one belonging 
    to this user, the value will change to a new one.

    Request Body params (**all params aren't required**): <br/>
    *::param::* username: str - The name of the user. <br/>
    *::param::* email: EmailStr - The email of the user, which **must match the email format**: _example@dom.ex_<br/>
    *::param::* password: str - The password of the user. <br/>
    *::param::* bio: str - The bio of the user. <br/>
    *::param::* image: HttpUrl - Link to a picture owned by the user, which **must match the url format**: _prtcl://dom.ex/_ <br/>
    """
    if user_update.username and user_update.username != current_user.username:
        if await check_username_is_taken(users_repo, user_update.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=strings.USERNAME_TAKEN,
            )

    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(users_repo, user_update.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=strings.EMAIL_TAKEN,
            )

    user = await users_repo.update_user(user=current_user, **user_update.dict())

    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))
    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token,
        ),
    )
