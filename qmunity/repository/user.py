import uuid

from tortoise.exceptions import DoesNotExist

from qmunity.models import Users
from qmunity.models.user import UserDto
from qmunity.models.user import UserPasswordHashDto
from qmunity.repository.exceptions import ObjectDoesNotFound


class UserRepository:
    """
    Users repository
    """
    def __init__(self) -> None:
        self.model = Users

    async def create_user(
        self,
        login: str,
        password_hash: str,
    ) -> UserDto:
        """
        Create new user in DB
        """
        user = await self.model.create(
            id=uuid.uuid4(),
            login=login,
            password_hash=password_hash,
        )
        await user.save()
        return user.get_dto()

    async def find_user_with_hash_by_login(
        self,
        login: str,
    ) -> UserPasswordHashDto:
        """
        Find user by login and get password hash
        """
        try:
            user = await self.model.get(login=login)
        except DoesNotExist:
            raise ObjectDoesNotFound()
        return user.get_dto_with_password_hash()

    async def find_user_by_id(self, id: str) -> UserDto:
        """
        Find user by id
        """
        try:
            user = await self.model.get(id=id)
        except DoesNotExist:
            raise ObjectDoesNotFound()
        return user.get_dto()
