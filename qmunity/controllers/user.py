import bcrypt
from fastapi import Depends
from pydantic import BaseModel, Field

from qmunity.controllers.obj import UserObj
from qmunity.repository.user import UserRepository


class UserRegistrationForm(BaseModel):
    login: str = Field(max_length=64, min_length=6)
    password: str = Field(max_length=64)


class UserController:
    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        super().__init__()
        self.user_repository = user_repository

    async def register_user(self, user_form: UserRegistrationForm) -> UserObj:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(
            password=user_form.password.encode("utf-8"), salt=salt
        )
        user = await self.user_repository.create_user(
            login=user_form.login, password_hash=password_hash.decode("utf-8")
        )
        return UserObj(
            id=user.id,
            login=user.login,
        )
