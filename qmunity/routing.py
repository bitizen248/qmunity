from fastapi import FastAPI

from qmunity.endpoints import auth
from qmunity.endpoints import cv
from qmunity.endpoints import user


def add_routing(app: FastAPI):
    app.include_router(user.router, prefix="/user")
    app.include_router(auth.router, prefix="/auth")
    app.include_router(cv.router, prefix="/cv")
