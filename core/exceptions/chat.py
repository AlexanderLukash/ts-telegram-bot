import json
from dataclasses import dataclass

from core.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class BaseWebException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def message(self):
        return "Error on the server side."

    @property
    def response_json(self) -> dict:
        return json.loads(self.response_content)

    @property
    def error_text(self) -> str:
        return self.response_json.get("detail", {}).get(
            "error",
            "Error on the server side.",
        )


@dataclass(frozen=True, eq=False)
class ChatListRequestError(BaseWebException):
    @property
    def message(self):
        return "Failed to retrieve chat list."


@dataclass(frozen=True, eq=False)
class ChatListenersRequestError(BaseWebException):
    @property
    def message(self):
        return "Failed to get a list of all listeners."


@dataclass(frozen=True, eq=False)
class AddChatListenersRequestError(BaseWebException):
    @property
    def message(self):
        return "Failed to add chat listener."


@dataclass(frozen=True, eq=False)
class GetChatInfoRequestError(BaseWebException):
    @property
    def message(self):
        return "Failed to receive chat information."


@dataclass(frozen=True, eq=False)
class SendMessageToChatRequestError(BaseWebException):
    @property
    def message(self):
        return "Failed to send a message to the chat."


@dataclass(frozen=True, eq=False)
class DeleteChatRequestError(BaseWebException):
    @property
    def message(self):
        return "Failed to delete the chat."


@dataclass(frozen=True, eq=False)
class CharInfoNotFoundError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self):
        return "Chat Info not found."


@dataclass(frozen=True, eq=False)
class ChatAlreadyExistsError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self):
        return "Chat already exists."


@dataclass(frozen=True, eq=False)
class ChatNotFoundByTelegramIDError(ApplicationException):
    telegram_chat_id: str

    @property
    def message(self):
        return f"Chat with telegram id {self.telegram_chat_id} not found."


@dataclass(frozen=True, eq=False)
class ChatNotFoundByWebIDError(ApplicationException):
    web_chat_id: str

    @property
    def message(self):
        return f"Chat with web id {self.web_chat_id} not found."


@dataclass(frozen=True, eq=False)
class ChatIsNotExistsError(ApplicationException):
    @property
    def message(self):
        return "Chat does not exist."
