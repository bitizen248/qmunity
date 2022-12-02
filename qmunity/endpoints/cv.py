from fastapi import APIRouter, Depends, Body

from qmunity.depends.mongodb_connection import mongodb_connection

router = APIRouter()


@router.post("/create")
async def register_user(
    mongo_connection = Depends(mongodb_connection),
) -> None:
    await mongo_connection.user.insert_one({"test": 1231})
