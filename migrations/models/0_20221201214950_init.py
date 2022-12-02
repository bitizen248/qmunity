from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
            "id" UUID NOT NULL  PRIMARY KEY
        );
        CREATE TABLE IF NOT EXISTS "authtokens" (
            "id" UUID NOT NULL  PRIMARY KEY,
            "token" VARCHAR(64) NOT NULL UNIQUE,
            "renew_token" VARCHAR(64) NOT NULL UNIQUE,
            "expiration" TIMESTAMPTZ NOT NULL,
            "renew_expiration" TIMESTAMPTZ NOT NULL,
            "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS "aerich" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "version" VARCHAR(255) NOT NULL,
            "app" VARCHAR(100) NOT NULL,
            "content" JSONB NOT NULL
        );"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "aerich";
        DROP TABLE IF EXISTS "authtokens";
        DROP TABLE IF EXISTS "users";
        """
