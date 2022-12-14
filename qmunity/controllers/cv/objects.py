from typing import List

from pydantic import BaseModel
from pydantic import Field

from qmunity.controllers.common_objects import BasicUserInfo


class CreateCvForm(BaseModel):
    name: str = Field()
    purpose: str = Field()
    tags: List[str] = Field()


class CreateCvResponse(BaseModel):
    id: str


class CvTagObject(BaseModel):
    id: str
    tag: str


class CvTagsResponse(BaseModel):
    tags: List[CvTagObject]


class CvListItem(BaseModel):
    id: str
    name: str
    purpose: str


class CvListResponse(BaseModel):
    cvs: List[CvListItem]


class CvDetailedResponse(BaseModel):
    id: str
    user: BasicUserInfo
    name: str
    purpose: str
    tags: List[str]
