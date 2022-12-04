from fastapi import APIRouter, Depends, Body

from qmunity.controllers.auth import AuthController
from qmunity.controllers.auth import AuthTokenResponse
from qmunity.controllers.auth import LoginForm
from qmunity.models.auth import AuthTokenDto

router = APIRouter()


@router.post("/login")
async def register_user(
    login_form: LoginForm = Body(),
    auth_controller: AuthController = Depends(),
) -> AuthTokenResponse:
    token = await auth_controller.login_user(
        login=login_form.login, password=login_form.password
    )
    return token
