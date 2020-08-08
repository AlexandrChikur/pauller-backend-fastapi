from pydantic import BaseModel, Field


class IDModelMixin(BaseModel):
    id: int = Field(0, alias="id")
