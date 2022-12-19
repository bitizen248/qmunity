from fastapi import APIRouter
from fastapi import FastAPI

from qmunity.endpoints import auth
from qmunity.endpoints import cv
from qmunity.endpoints import user


def add_routing(app: FastAPI):
    """
    Init app routing
    """
    router = APIRouter(prefix="/v1")
    router.include_router(user.router, prefix="/user")
    router.include_router(auth.router, prefix="/auth")
    router.include_router(cv.router, prefix="/cv")
    app.include_router(router)
