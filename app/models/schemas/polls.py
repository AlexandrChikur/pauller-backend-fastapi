from datetime import datetime
from typing import List, Optional

import pytz
from pydantic import BaseModel, validator

from app.models.common import IDModelMixin


class Poll(BaseModel):
    title: str
    description: Optional[str] = ""
    created_at: datetime
    start_at: datetime
    finish_at: datetime
    poll_type: str = "single"
    anonymously: bool = False

    @validator("poll_type")
    def correct_value_of_poll_type(cls, v: str):
        if v.lower() not in ["single", "multiple", "text"]:
            raise ValueError("poll_type must be equal one of: single, multiple or text")

        return v.lower()

    def is_active(self):
        return all(
            [
                self.start_at < pytz.UTC.localize(datetime.now()),
                self.finish_at > pytz.UTC.localize(datetime.now()),
            ]
        )


class PollInDB(Poll, IDModelMixin):
    author_id: int


class PollInResponse(BaseModel):
    count: int
    next: Optional[str]
    prev: Optional[str]
    results: List[PollInDB]
