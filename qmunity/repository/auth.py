import uuid
from datetime import datetime

from tortoise.exceptions import DoesNotExist

from qmunity.models import AuthTokens
from qmunity.models.auth import AuthTokenDto
from qmunity.models.user import UserDto
from qmunity.repository.exceptions import ObjectDoesNotFound


class AuthRepository:
    def __init__(self) -> None:
        self.model = AuthTokens

    async def create_auth_token(
        self,
        id: uuid.uuid4,
        user_id: uuid.uuid4,
        token: str,
        renew_token: str,
        expiration: datetime,
        renew_expiration: datetime,
    ) -> AuthTokenDto:
        token = await self.model.create(
            id=id,
            user_id=user_id,
            token=token,
            renew_token=renew_token,
            expiration=expiration,
            renew_expiration=renew_expiration,
        )
        return token.get_dto()

    async def find_token(self, token: str) -> UserDto:
        try:
            token = await self.model.get(token=token).prefetch_related("user")
        except DoesNotExist:
            raise ObjectDoesNotFound()
        return token.user.get_dto()
