"""
Objects for CV controllers
"""
from typing import List

from pydantic import BaseModel
from pydantic import Field

from qmunity.controllers.common_objects import BasicUserInfo


# /create objects
class CreateCvForm(BaseModel):
    """
    CV creation form
    """

    name: str = Field()
    purpose: str = Field()
    tags: List[str] = Field()


class CreateCvResponse(BaseModel):
    """
    Result of creating CV
    """

    id: str


# /tags objects
class CvTagObject(BaseModel):
    """
    List item of CV tag object
    """

    id: str
    tag: str


class CvTagsResponse(BaseModel):
    """
    Tags list response
    """

    tags: List[CvTagObject]


# /list objects
class CvListItem(BaseModel):
    """
    List item of CV
    """

    id: str
    name: str
    purpose: str


class CvListResponse(BaseModel):
    """
    List of CVs
    """

    cvs: List[CvListItem]


# /{id} objects
class CvDetailedResponse(BaseModel):
    """
    Detailed CV object
    """

    id: str
    user: BasicUserInfo
    name: str
    purpose: str
    tags: List[str]
