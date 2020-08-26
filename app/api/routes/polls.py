from fastapi import APIRouter, Body, Depends, Query, Request, status
from fastapi.responses import JSONResponse

from app.api.dependencies.auth import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.api.errors.permissions import PermissionDeniedError
from app.db.repositories.polls import PollsRepository
from app.models.schemas.polls import Poll, PollInDB, PollInResponse
from app.resources import strings
from app.api.dependencies.permissions import (
    get_active_permissionizer,
    get_admin_permissionizer,
)
from app.models.schemas.users import UserInDB


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PollInResponse,
    summary="Get Exists Polls",
    name="polls:get_polls",
    dependencies=[
        Depends(get_admin_permissionizer(required=False)),
        Depends(get_active_permissionizer()),
        Depends(get_current_user_authorizer())
    ],
)
async def get_polls(
    request: Request,
    poll_repo: PollsRepository = Depends(get_repository(PollsRepository)),
    limit: int = Query(
        None, title="limit", description="Maximum amount of polls to be shown"
    ),
    offset: int = Query(
        None, title="offset", description="Poll number from which polls will be shown"
    ),
    all: bool = Query(
        False,
        title="Get all polls function",
        description="Turn it True to get all polls, **allowed only for admin**",
    ),
) -> PollInResponse:
    """
    Method for **get** the polls. <br/><br/>
    Allowed for ```active``` user. To use the *all* parameter, the user must have ```administrator``` access. <br/><br/>
    For the active user will be returned a list of ```active polls```. For admin allowed to get all polls include ```inactive```. <br/>

    Query params (**all params aren't required**): <br/>
    *::param::* limit: int - Maximum amount of polls to be shown. <br/>
    *::param::* offset: int - Poll number from which polls will be shown. <br/>
    *::param::* all: bool - Turn it True to get all polls, **allowed only for admin**. <br/>
    """
    if all:
        if request.app.state.admin_user_requested:
            return await poll_repo.get_all_polls()
        raise PermissionDeniedError(sub="user is not admin")

    return await poll_repo.get_polls(limit=limit, offset=offset, is_admin=request.app.state.admin_user_requested)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=Poll,
    summary="Create the poll",
    name="polls:create_poll",
    dependencies=[Depends(get_active_permissionizer())],
)
async def create_poll(
    poll_create: Poll = Body(..., embed=True, alias="poll"),
    current_user: UserInDB = Depends(get_current_user_authorizer()),
    poll_repo: PollsRepository = Depends(get_repository(PollsRepository)),
) -> Poll:
    """
    Method for **create** the poll. <br/><br/>
    Allowed for ```active``` user.

    Request Body params:<br/>
    *::param::*           title: str -  The title of the poll. (**REQUIRED**) <br/>
    *::param::*     description: str -  The description of the poll. <br/>
    *::param::* created_at: datetime -  The time when the poll is created. (**REQUIRED**) <br/>
    *::param::*   start_at: datetime -  Time when you can start voting in the poll. (**REQUIRED**) <br/>
    *::param::*  finish_at: datetime -  The time when the poll will be closed for voting. (**REQUIRED**) <br/>
    *::param::*       poll_type: str -  Type of the poll. Can be one of "single", "text" or "multiple". (**REQUIRED**) <br/>
    *::param::*    anonymously: bool -  A parameter that makes the poll anonymous. Can be True or False. False by default. <br/>
    """
    poll_with_author_id = PollInDB(**poll_create.dict(), author_id=current_user.id)

    return await poll_repo.create_poll(**poll_with_author_id.dict())


@router.delete(
    "/delete/{id}/",
    status_code=status.HTTP_200_OK,
    summary="Delete the poll",
    name="polls:delete_poll",
    dependencies=[Depends(get_admin_permissionizer()), Depends(get_current_user_authorizer())],
    tags=["admin"],
)
async def delete_poll(
    id: int,
    poll_repo: PollsRepository = Depends(get_repository(PollsRepository)),
) -> JSONResponse:
    """
    Method for **delete** the poll from db.<br/> <br/>
    Allowed for ```admin``` only.

    *::param::* id: int  - id belonging to the poll to be deleted (**REQUIRED**)  <br/><br/>

    Returns a JSONResponse with static content: "the poll was successfully deleted" and status code=200.
    """
    await poll_repo.delete_poll(id=id)

    return JSONResponse(content=strings.POLL_DELETED, status_code=status.HTTP_200_OK)
