from motor import motor_asyncio as motor

from qmunity.config import MONGO_CONFIG


def mongodb_connection() -> motor.AsyncIOMotorDatabase:
    """
    MongoDB's connection wit qmunity DB
    """
    client = motor.AsyncIOMotorClient(MONGO_CONFIG.get_connection_url())
    try:
        yield client.qmunity
    finally:
        client.close()
