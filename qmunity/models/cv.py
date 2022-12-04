from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import Field
from tortoise import models
from tortoise import fields


class CvTag(models.Model):
    id = fields.UUIDField(pk=True)
    tag = fields.CharField(max_length=32)
    parent = fields.ForeignKeyField("models.CvTag", null=True)


class CvObject(BaseModel):
    id: str | None = Field(exclude=True)
    created_at: datetime
    modified_at: datetime | None
    user_id: str
    name: str
    purpose: str

    def __init__(__pydantic_self__, _id=None, **data: Any) -> None:
        super().__init__(id=str(_id) if _id is not None else None, **data)
