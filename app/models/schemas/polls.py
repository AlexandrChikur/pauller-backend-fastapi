from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, validator

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


class PollInDB(Poll, IDModelMixin):
    author_id: int


class PollInResponse(BaseModel):
    count: int
    next: HttpUrl
    prev: HttpUrl
    results: List[PollInDB]
