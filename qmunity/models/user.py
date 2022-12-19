from pydantic import BaseModel
from tortoise import fields, models


class Users(models.Model):
    """
    Users model
    """
    id = fields.UUIDField(pk=True)
    login = fields.CharField(max_length=64, unique=True)
    password_hash = fields.CharField(max_length=60)

    def get_dto(self) -> "UserDto":
        return UserDto(id=str(self.id), login=self.login)

    def get_dto_with_password_hash(self) -> "UserPasswordHashDto":
        return UserPasswordHashDto(
            id=str(self.id),
            login=self.login,
            password_hash=self.password_hash,
        )


class UserDto(BaseModel):
    """
    User model DTO
    """
    id: str
    login: str


class UserPasswordHashDto(UserDto):
    """
    User model DTO with hash
    """
    password_hash: str

    def get_password_salt(self) -> str:
        return self.password_hash[:29]
