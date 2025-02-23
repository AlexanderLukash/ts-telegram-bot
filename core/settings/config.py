from functools import lru_cache

from pydantic_settings import BaseSettings

import environ

env = environ.Env()
environ.Env.read_env(".env")


class Config(BaseSettings):
    BOT_TOKEN: str = env("BOT_TOKEN")
    WEB_API_BASE_URL: str = env("WEB_API_BASE_URL", default="http://localhost:8000")
    KAFKA_BROKER_URL: str = env("KAFKA_BROKER_URL", default="kafka:29092")
    NEW_MESSAGE_TOPIC: str = env("NEW_MESSAGE_TOPIC", default="new-messages-topic")
    KAFKA_GROUP_ID: str = env("KAFKA_GROUP_ID", default="tg-bot")
    GREETING_TEXT: str = env(
        "GREETING_TEXT",
        default=(
            "Welcome to a technical support chat, choose a chat to work with a client."
            "Get a list of all chats: /chats"
        ),
    )


@lru_cache(1)
def get_config() -> Config:
    return Config()
