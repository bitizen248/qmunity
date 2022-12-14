from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends

from qmunity.controllers.cv import CreateCvForm
from qmunity.controllers.cv import CreateCvResponse
from qmunity.controllers.cv import CvController
from qmunity.controllers.cv import CvListResponse
from qmunity.controllers.cv import CvTagsResponse
from qmunity.controllers.obj import UserObj
from qmunity.depends.auth import auth_user

router = APIRouter()


@router.get("/tags")
async def get_tags(
    parent_id: str | None = None,
    offset: int = 0,
    limit: int = 50,
    cv_controller: CvController = Depends(),
) -> CvTagsResponse:
    return await cv_controller.get_cv_tags(
        parent_id=parent_id, offset=offset, limit=limit
    )


@router.post("/create", status_code=201)
async def create_cv(
    user: UserObj = Depends(auth_user),
    form: CreateCvForm = Body(),
    cv_controller: CvController = Depends(),
) -> CreateCvResponse:
    res = await cv_controller.create_cv(
        user=user,
        form=form,
    )
    return res


@router.get("/list")
async def get_cvs_list(
    offset: int = 0,
    limit: int = 50,
    user_id: str | None = None,
    user: UserObj = Depends(auth_user),
    cv_controller: CvController = Depends(),
) -> CvListResponse:
    res = await cv_controller.get_users_cv(
        user_id=user_id or user.id,
        offset=offset,
        limit=limit,
    )
    return res
