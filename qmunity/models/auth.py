from datetime import datetime

from pydantic import BaseModel
from tortoise import fields
from tortoise import models


class AuthTokens(models.Model):
    """
    Model for storing users token
    """
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.Users")
    token = fields.CharField(max_length=64, unique=True)
    renew_token = fields.CharField(max_length=64, unique=True)
    expiration = fields.DatetimeField()
    renew_expiration = fields.DatetimeField()

    def get_dto(self) -> "AuthTokenDto":
        return AuthTokenDto(
            token=self.token,
            renew_token=self.renew_token,
            expiration=self.expiration,
        )


class AuthTokenDto(BaseModel):
    """
    Auth token DTO
    """
    token: str
    renew_token: str
    expiration: datetime
