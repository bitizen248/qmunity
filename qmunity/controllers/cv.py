from datetime import datetime

from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field

from qmunity.controllers.obj import UserObj
from qmunity.models.cv import CvObject
from qmunity.repository.cv import CvRepository


class CreateCvForm(BaseModel):
    name: str = Field()
    purpose: str = Field()


class CvController:
    def __init__(
        self,
        cv_repository: CvRepository = Depends()
    ) -> None:
        self.cv_repository = cv_repository

    async def create_cv(self, user: UserObj, form: CreateCvForm):
        users_cvs = await self.cv_repository.find_users_cv(user.id)
        names = set([cv.name for cv in users_cvs])
        if form.name in names:
            raise HTTPException(status_code=400, detail="CV with such name already exists")
        now = datetime.now()
        return await self.cv_repository.create_cv(
            CvObject(
                user_id=user.id,
                created_at=now,
                **form.dict()
            )
        )
