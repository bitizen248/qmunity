from typing import List

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from qmunity.depends import mongodb_connection
from qmunity.models import CvTag
from qmunity.models.cv import CvObject


class CvRepository:
    def __init__(
        self,
        mongo_connection: AsyncIOMotorDatabase = Depends(mongodb_connection),
    ) -> None:
        self.model = CvTag
        self.mongo_connection = mongo_connection

    async def create_cv(self, cv: CvObject) -> CvObject:
        res = await self.mongo_connection["cv"].insert_one(cv.dict())
        cv.id = str(res.inserted_id)
        return cv

    async def find_users_cv(self, user_id: str) -> List[CvObject]:
        res = []
        async for obj in self.mongo_connection["cv"].find({"user_id": user_id}):
            res.append(CvObject(**obj))
        return res