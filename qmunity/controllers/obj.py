from pydantic import BaseModel


class UserObj(BaseModel):
    id: str
    login: str
