from fastapi import Depends
from fastapi import Header

from qmunity.controllers.auth import AuthController
from qmunity.controllers.user import UserObj


async def auth_user(
    x_token: str = Header(),
    auth_controller: AuthController = Depends(),
) -> UserObj:
    """
    Auth user from X-Token header
    """
    user = await auth_controller.auth_user(x_token)
    return user
