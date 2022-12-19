from datetime import datetime
from typing import List

from pydantic import BaseModel
from tortoise import models
from tortoise import fields

from qmunity.models.mongo_model import MongoModel


class CvTag(models.Model):
    """
    Model for storing CV tags
    """
    id = fields.UUIDField(pk=True)
    tag = fields.CharField(max_length=32)
    parent = fields.ForeignKeyField("models.CvTag", null=True)
    sort = fields.IntField(default=500)

    def get_dto(self) -> "CvTagDto":
        return CvTagDto(id=str(self.id), tag=self.tag)


class CvTagDto(BaseModel):
    """
    CV tag DTO
    """
    id: str
    tag: str


class CvDto(MongoModel):
    """
    Mongo model for storing users CV
    """
    created_at: datetime
    modified_at: datetime | None
    user_id: str
    name: str
    purpose: str
    tags: List[str]
