from fastapi import Depends
from fastapi import Header

from qmunity.controllers.auth import AuthController
from qmunity.repository.user import UserDto


async def auth_user(
    x_token: str = Header(),
    auth_controller: AuthController = Depends(),
) -> UserDto:
    user = await auth_controller.auth_user(x_token)
    return user