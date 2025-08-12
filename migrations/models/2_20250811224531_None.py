from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(256) NOT NULL,
    "first_name" VARCHAR(50),
    "last_name" VARCHAR(50),
    "is_online" INT NOT NULL DEFAULT 0,
    "last_seen" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "chats" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user1_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "user2_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_chats_user1_i_e4cc3d" UNIQUE ("user1_id", "user2_id")
);
CREATE TABLE IF NOT EXISTS "global_messages" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "message" TEXT NOT NULL,
    "username" VARCHAR(256) NOT NULL,
    "user_full_name" VARCHAR(512) NOT NULL,
    "sendet_data" TIMESTAMP NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "messages" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_read" INT NOT NULL DEFAULT 0,
    "chat_id" INT NOT NULL REFERENCES "chats" ("id") ON DELETE CASCADE,
    "sender_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
