from fastapi import APIRouter, Depends, Body

from qmunity.controllers.user import UserController
from qmunity.controllers.user import UserRegistrationForm
from qmunity.depends.auth import auth_user
from qmunity.models.user import UserDto

router = APIRouter()


@router.post("/register", status_code=201)
async def register_user(
    user: UserRegistrationForm = Body(),
    user_controller: UserController = Depends(),
):
    await user_controller.register_user(user)

    return {"success": True}


@router.get("/me")
async def get_me(user: UserDto = Depends(auth_user)):
    return user
