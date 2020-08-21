from fastapi import APIRouter, Body, Depends, Query, Request, status

from app.api.dependencies.auth import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.api.errors.permissions import PermissionDeniedError
from app.db.repositories.polls import PollsRepository
from app.models.schemas.polls import Poll, PollInDB, PollInResponse
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
    ],
)
async def get_polls(
    request: Request,
    current_user: UserInDB = Depends(get_current_user_authorizer()),
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
    """ Some description """
    if all:
        if request.app.state.admin_user_requested:
            return await poll_repo.get_all_polls()
        raise PermissionDeniedError(sub="user is not admin")

    return await poll_repo.get_polls(limit=limit, offset=offset)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=Poll,
    summary="Create the poll",
    name="polls:create_poll",
)
async def create_poll(
    poll_create: Poll = Body(..., embed=True, alias="poll"),
    current_user: UserInDB = Depends(get_current_user_authorizer()),
    poll_repo: PollsRepository = Depends(get_repository(PollsRepository)),
) -> Poll:
    """ Description """
    poll_with_author_id = PollInDB(**poll_create.dict(), author_id=current_user.id)

    return await poll_repo.create_poll(**poll_with_author_id.dict())
