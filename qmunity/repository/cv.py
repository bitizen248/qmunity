import uuid
from typing import List

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from qmunity.depends import mongodb_connection
from qmunity.models import CvTag
from qmunity.models.cv import CvDto
from qmunity.models.cv import CvTagDto
from qmunity.repository.exceptions import ObjectDoesNotFound


class CvTagsRepository:
    """
    Repository for CV tags
    """
    def __init__(self) -> None:
        self.model = CvTag

    async def get_cv_tags(
        self, parent_id: str | None = 0, limit: int = 50, offset: int = 0
    ) -> List[CvTagDto]:
        """
        Get CV tags
        """
        tags = (
            await self.model.filter(parent_id=parent_id)
            .order_by("sort")
            .limit(limit)
            .offset(offset)
        )
        return [tag.get_dto() for tag in tags]


class CvRepository:
    """
    Repository for CVs
    """
    def __init__(
        self,
        mongo_connection: AsyncIOMotorDatabase = Depends(mongodb_connection),
    ) -> None:
        self.mongo_connection = mongo_connection

    async def create_cv(self, cv: CvDto) -> CvDto:
        """
        Create new CV in DB
        :param cv:
        :return:
        """
        res = await self.mongo_connection["cv"].insert_one(cv.dict())
        cv.id = str(res.inserted_id)
        return cv

    async def find_users_cv(
        self, user_id: str, limit: int = 50, offset: int = 0
    ) -> List[CvDto]:
        """
        Find users CVs
        """
        res = []
        async for obj in self.mongo_connection["cv"].find(
            {"user_id": user_id}
        ).limit(limit).skip(offset):
            res.append(CvDto(**obj))
        return res

    async def find_cv_by_id(self, id):
        """
        Find specific CV by id
        """
        cv = await self.mongo_connection["cv"].find_one({"_id": id})
        if cv is None:
            raise ObjectDoesNotFound()
        return CvDto(**cv)
