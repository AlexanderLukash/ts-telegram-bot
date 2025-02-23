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
