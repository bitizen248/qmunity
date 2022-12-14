from pydantic import BaseModel


class BasicUserInfo(BaseModel):
    id: str
    login: str
