from fastapi import APIRouter
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from qmunity.depends import mongodb_connection

router = APIRouter()


@router.post("/create")
async def create_cv(
    mongo_connection: AsyncIOMotorDatabase = Depends(mongodb_connection),
) -> None:
    await mongo_connection.user.insert_one({"test": 1231})
