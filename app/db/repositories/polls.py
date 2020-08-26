from datetime import datetime
from typing import Optional

from app.db.queries.polls import (
    CREATE_POLL,
    GET_ALL_POLLS,
    GET_POLLS,
    GET_POLLS_COUNT,
    DELETE_POLL_BY_ID,
)
from app.db.repositories.base import BaseRepository
from app.models.schemas.polls import PollInDB, PollInResponse


class PollsRepository(BaseRepository):
    async def create_poll(
        self,
        *,
        id: int,
        title: str,
        description: Optional[str],
        author_id: int,
        created_at: datetime,
        start_at: datetime,
        finish_at: datetime,
        poll_type: str,
        anonymously: bool,
    ) -> PollInDB:
        poll = PollInDB(
            title=title,
            description=description,
            author_id=author_id,
            created_at=created_at,
            start_at=start_at,
            finish_at=finish_at,
            poll_type=poll_type,
            anonymously=anonymously,
        )

        await self._conn.execute(
            CREATE_POLL,
            poll.title,
            poll.description,
            poll.author_id,
            poll.created_at,
            poll.start_at,
            poll.finish_at,
            poll.poll_type,
            poll.anonymously,
        )

        return poll

    async def get_count_of_polls(self) -> int:
        return (await self._conn.fetchrow(GET_POLLS_COUNT))["count"]

    async def get_all_polls(self) -> PollInResponse:
        polls = await self._conn.fetch(GET_ALL_POLLS)

        return PollInResponse(
            count=len(polls),
            next="not implemented yet",
            prev="not implemented yet",
            results=[PollInDB(**poll) for poll in polls],
        )

    async def get_polls(
        self, *, limit: Optional[int] = None, offset: Optional[int] = None, is_admin: Optional[bool] = False,
    ) -> PollInResponse:
        polls = await self._conn.fetch(GET_POLLS, offset, limit)

        if is_admin:
            results = [PollInDB(**poll) for poll in polls if PollInDB(**poll)]
        else:
            results = [PollInDB(**poll) for poll in polls if PollInDB(**poll).is_active()]


        return PollInResponse(
            count=len(polls),
            next="not implemented yet",
            prev="not implemented yet",
            results=results,
        )

    async def delete_poll(self, *, id: int) -> None:
        await self._conn.execute(DELETE_POLL_BY_ID, id)
