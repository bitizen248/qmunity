from datetime import datetime

from fastapi import Depends
from fastapi import HTTPException

from qmunity.controllers.common_objects import BasicUserInfo
from qmunity.controllers.cv.objects import CreateCvForm
from qmunity.controllers.cv.objects import CreateCvResponse
from qmunity.controllers.cv.objects import CvDetailedResponse
from qmunity.controllers.cv.objects import CvListItem
from qmunity.controllers.cv.objects import CvListResponse
from qmunity.controllers.cv.objects import CvTagObject
from qmunity.controllers.cv.objects import CvTagsResponse
from qmunity.controllers.obj import UserObj
from qmunity.models.cv import CvDto
from qmunity.repository.cv import CvRepository
from qmunity.repository.cv import CvTagsRepository
from qmunity.repository.exceptions import ObjectDoesNotFound
from qmunity.repository.user import UserRepository


class CvController:
    def __init__(
        self,
        cv_tag_repository: CvTagsRepository = Depends(),
        cv_repository: CvRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.user_repository = user_repository
        self.cv_tag_repository = cv_tag_repository
        self.cv_repository = cv_repository

    async def get_cv_tags(
        self,
        parent_id: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> CvTagsResponse:
        tags = await self.cv_tag_repository.get_cv_tags(
            parent_id=parent_id,
            limit=limit,
            offset=offset,
        )
        tags_obj = [
            CvTagObject(
                id=tag.id,
                tag=tag.tag,
            )
            for tag in tags
        ]
        return CvTagsResponse(tags=tags_obj)

    async def create_cv(
        self,
        user: UserObj,
        form: CreateCvForm,
    ) -> CreateCvResponse:
        users_cvs = await self.cv_repository.find_users_cv(user.id)
        names = set([cv.name for cv in users_cvs])
        if form.name in names:
            raise HTTPException(
                status_code=400, detail="CV with such name already exists"
            )
        now = datetime.now()
        cv = await self.cv_repository.create_cv(
            CvDto(user_id=user.id, created_at=now, **form.dict())
        )
        return CreateCvResponse(id=cv.id)

    async def get_users_cv(
        self,
        user_id: str,
        offset: int = 0,
        limit: int = 50,
    ) -> CvListResponse:
        try:
            await self.user_repository.find_user_by_id(user_id)
        except ObjectDoesNotFound:
            raise HTTPException(status_code=404, detail="User not found")
        cvs_dto = await self.cv_repository.find_users_cv(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )
        return CvListResponse(
            cvs=[
                CvListItem(
                    id=cv.id,
                    name=cv.name,
                    purpose=cv.purpose,
                )
                for cv in cvs_dto
            ]
        )

    async def get_cv(self, cv_id: str) -> CvDetailedResponse:
        try:
            cv_dto = await self.cv_repository.find_cv_by_id(cv_id)
        except ObjectDoesNotFound:
            raise HTTPException(status_code=404, detail="CV not found")
        user_dto = await self.user_repository.find_user_by_id(cv_dto.user_id)
        return CvDetailedResponse(
            id=cv_dto.id,
            user=BasicUserInfo(
                id=user_dto.id,
                login=user_dto.login,
            ),
            name=cv_dto.name,
            purpose=cv_dto.purpose,
            tags=cv_dto.tags
        )
