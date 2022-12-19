from pydantic import BaseModel


class BasicUserInfo(BaseModel):
    """
    Object for short user info
    """

    id: str
    login: str
