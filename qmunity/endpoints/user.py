from fastapi import APIRouter, Depends, Body

from qmunity.controllers.obj import UserObj
from qmunity.controllers.user import UserController
from qmunity.controllers.user import UserRegistrationForm
from qmunity.depends.auth import auth_user
from qmunity.endpoints.responses import SimpleResponse
from qmunity.models.user import UserDto

router = APIRouter()


@router.post("/register", status_code=201)
async def register_user(
    user: UserRegistrationForm = Body(),
    user_controller: UserController = Depends(),
) -> SimpleResponse:
    await user_controller.register_user(user)

    return SimpleResponse()


@router.get("/me")
async def get_me(user: UserObj = Depends(auth_user)) -> UserObj:
    return user
