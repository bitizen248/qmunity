from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "cvtag" ADD "sort" INT NOT NULL  DEFAULT 500;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "cvtag" DROP COLUMN "sort";"""
