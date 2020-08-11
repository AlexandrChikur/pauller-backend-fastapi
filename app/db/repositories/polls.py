from datetime import datetime
from typing import Optional

from app.db.queries.polls import CREATE_POLL
from app.db.repositories.base import BaseRepository
from app.models.schemas.polls import PollInDB


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
