from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BOT_TOKEN: str = Field(alias="BOT_TOKEN")
    WEB_API_BASE_URL: str = Field(
        alias="WEB_API_BASE_URL",
        default="http://localhost:8000",
    )
    KAFKA_BROKER_URL: str = Field(alias="KAFKA_BROKER_URL", default="kafka:29092")
    NEW_MESSAGE_TOPIC: str = Field(
        alias="NEW_MESSAGE_TOPIC",
        default="new-messages-topic",
    )
    KAFKA_GROUP_ID: str = Field(alias="KAFKA_GROUP_ID", default="tg-bot")
    GREETING_TEXT: str = Field(
        alias="GREETING_TEXT",
        default=(
            "Welcome to a technical support chat, choose a chat to work with a client."
            "Get a list of all chats: /chats"
        ),
    )
    DATABASE_NAME: str = Field(alias="DATABASE_NAME", default="test.db")


@lru_cache(1)
def get_config() -> Config:
    return Config()
