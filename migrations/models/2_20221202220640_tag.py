from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "cvtag" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "tag" VARCHAR(32) NOT NULL,
    "parent_id" UUID REFERENCES "cvtag" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "cvtag";"""
