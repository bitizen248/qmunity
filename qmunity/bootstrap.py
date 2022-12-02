import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from qmunity.config import POSTGRES_CONFIG
from qmunity.routing import add_routing

app = FastAPI()
add_routing(app)
register_tortoise(
    app,
    db_url=POSTGRES_CONFIG.get_connection_url(),
    modules={"models": ["qmunity.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run("qmunity.bootstrap:app", port=8080)
