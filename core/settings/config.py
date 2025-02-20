from pydantic_settings import BaseSettings

import environ

env = environ.Env()
environ.Env.read_env(".env")


class Config(BaseSettings):
    BOT_TOKEN: str = env("BOT_TOKEN")
    WEB_API_BASE_URL: str = env("WEB_API_BASE_URL", default="http://localhost:8000")
    GREETING_TEXT: str = env(
        "GREETING_TEXT",
        default=(
            "Welcome to a technical support chat, choose a chat to work with a client."
            "Get a list of all chats: /chats"
        ),
    )
