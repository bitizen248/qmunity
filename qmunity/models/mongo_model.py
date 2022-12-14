import abc
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class MongoModel(BaseModel, abc.ABC):
    id: str | None = Field(exclude=True)

    def __init__(__pydantic_self__, _id=None, **data: Any) -> None:
        super().__init__(id=str(_id) if _id is not None else None, **data)
