import random
import string
import uuid
from datetime import datetime
from datetime import timedelta

import bcrypt
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel

from qmunity.controllers.obj import UserObj
from qmunity.repository.auth import AuthRepository
from qmunity.repository.exceptions import ObjectDoesNotFound
from qmunity.repository.user import UserRepository


class LoginForm(BaseModel):
    """
    Form for authorization
    """

    login: str
    password: str


class AuthTokenResponse(BaseModel):
    """
    Response for authorization
    """

    token: str
    renew_token: str
    expiration: int


class AuthController:
    """
    Controller for authentication and authorization
    """

    def __init__(
        self,
        auth_repository: AuthRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.user_repository = user_repository
        self.auth_repository = auth_repository

    @staticmethod
    def _generate_random_string(length: int) -> str:
        """
        Generate random string of characters
        Used for generating tokens
        """
        letters = string.ascii_letters + string.digits
        return "".join(random.choice(letters) for _ in range(length))

    async def login_user(self, login: str, password: str) -> AuthTokenResponse:
        """
        Authorize user with login and password
        """
        try:
            user = await self.user_repository.find_user_with_hash_by_login(
                login
            )
        except ObjectDoesNotFound:
            raise HTTPException(
                status_code=401, detail="Wrong login or password"
            )
        salt = user.get_password_salt().encode("utf-8")
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
        if password_hash.decode("utf-8") != user.password_hash:
            raise HTTPException(
                status_code=401, detail="Wrong login or password"
            )
        now = datetime.now()
        token = await self.auth_repository.create_auth_token(
            id=uuid.uuid4(),
            user_id=user.id,
            token=self._generate_random_string(64),
            renew_token=self._generate_random_string(64),
            expiration=now + timedelta(days=30),
            renew_expiration=now + timedelta(days=60),
        )
        return AuthTokenResponse(
            token=token.token,
            renew_token=token.renew_token,
            expiration=token.expiration.timestamp(),
        )

    async def auth_user(self, token: str) -> UserObj:
        """
        Authenticate user with X-Token
        """
        try:
            user = await self.auth_repository.find_token(token)
        except ObjectDoesNotFound:
            raise HTTPException(
                status_code=401, detail="Method requires authorization"
            )
        return UserObj(id=user.id, login=user.login)
