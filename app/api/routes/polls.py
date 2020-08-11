from fastapi import APIRouter, Body, Depends, status, Query

from app.api.dependencies.auth import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.db.repositories.polls import PollsRepository
from app.db.errors.users import PermissionDeniedError
from app.db.repositories.users import UsersRepository
from app.models.schemas.polls import Poll, PollInDB, PollInResponse
from app.models.schemas.users import UserInDB

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    #response_model=PollInResponse,
    summary="Get Exists Polls",
    name="polls:get_polls",
)
async def get_polls(
    current_user: UserInDB = Depends(get_current_user_authorizer(required=False)),
    poll_repo: PollsRepository = Depends(get_repository(PollsRepository)),
    limit: int = Query(None, alias="alias", title="title", description="description"),
    offset: int = Query(None, alias="alias", title="title", description="description"), 
):
    """ Some description """
    
    return {} 


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

