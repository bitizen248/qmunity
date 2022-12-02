from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "password_hash" VARCHAR(60) NOT NULL;
        ALTER TABLE "users" ADD "login" VARCHAR(64) NOT NULL UNIQUE;
        CREATE UNIQUE INDEX "uid_users_login_d5b5e4" ON "users" ("login");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_users_login_d5b5e4";
        ALTER TABLE "users" DROP COLUMN "password_hash";
        ALTER TABLE "users" DROP COLUMN "login";"""
