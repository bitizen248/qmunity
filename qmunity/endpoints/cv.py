from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends

from qmunity.controllers.cv import CreateCvForm
from qmunity.controllers.cv import CvController
from qmunity.controllers.obj import UserObj
from qmunity.depends.auth import auth_user
from qmunity.endpoints.responses import SimpleResponse

router = APIRouter()


@router.post("/create", status_code=201)
async def create_cv(
    user: UserObj = Depends(auth_user),
    form: CreateCvForm = Body(),
    cv_controller: CvController = Depends(),
) -> SimpleResponse:
    return (await cv_controller.create_cv(
        user=user,
        form=form,
    )).dict(include={"id": True})

    return SimpleResponse()
