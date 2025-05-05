from abc import ABC, abstractmethod
from dataclasses import dataclass
from urllib.parse import urljoin

from httpx import AsyncClient

from core.dtos.chats import ChatListItemDTO, ChatListenerDTO
from core.exceptions.chat import (
    ChatListRequestError,
    ChatListenersRequestError,
    AddChatListenersRequestError,
    GetChatInfoRequestError,
    SendMessageToChatRequestError,
)
from core.services.converters.chats import (
    convert_chat_response_to_chat_dto,
    convert_chat_listener_response_to_listener_dto,
)
from core.settings.constants import (
    CHAT_LIST_URI,
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    CHAT_LISTENERS_URI,
    ADD_LISTENER_TO_CHAT_URI,
    CHAT_INFO_URL,
    SEND_MESSAGE_TO_CHAT_URI,
)


@dataclass
class BaseChatWebService(ABC):
    http_client: AsyncClient
    base_url: str

    @abstractmethod
    async def get_all_chats(self) -> list[ChatListItemDTO]: ...

    @abstractmethod
    async def get_chat_listeners(self, chat_oid: str) -> list[ChatListenerDTO]: ...

    @abstractmethod
    async def add_listener(self, telegram_chat_id: str, chat_oid: str) -> None: ...

    @abstractmethod
    async def get_chat_info(self, chat_oid: str) -> ChatListItemDTO: ...

    @abstractmethod
    async def send_message_to_chat(self, chat_oid: str, text: str) -> None: ...


@dataclass
class ChatWebService(BaseChatWebService):
    async def get_all_chats(self) -> list[ChatListItemDTO]:
        response = await self.http_client.get(
            url=urljoin(base=self.base_url, url=CHAT_LIST_URI),
            params={
                "limit": DEFAULT_LIMIT,
                "offset": DEFAULT_OFFSET,
            },
        )

        if not response.is_success:
            raise ChatListRequestError(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )

        json_data = response.json()
        return [
            convert_chat_response_to_chat_dto(chat_data=chat_data)
            for chat_data in json_data["items"]
        ]

    async def get_chat_listeners(self, chat_oid: str) -> list[ChatListenerDTO]:
        response = await self.http_client.get(
            url=urljoin(
                base=self.base_url,
                url=CHAT_LISTENERS_URI.format(chat_oid=chat_oid),
            ),
        )

        if not response.is_success:
            raise ChatListenersRequestError(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )

        json_data = response.json()
        return [
            convert_chat_listener_response_to_listener_dto(listener_data=listener_data)
            for listener_data in json_data
        ]

    async def add_listener(self, telegram_chat_id: str, chat_oid: str) -> None:
        response = await self.http_client.post(
            url=urljoin(
                base=self.base_url,
                url=ADD_LISTENER_TO_CHAT_URI.format(chat_oid=chat_oid),
            ),
            json={
                "telegram_chat_id": telegram_chat_id,
            },
        )

        if not response.is_success:
            raise AddChatListenersRequestError(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )

    async def get_chat_info(self, chat_oid: str) -> ChatListItemDTO:
        response = await self.http_client.get(
            url=urljoin(
                base=self.base_url,
                url=CHAT_INFO_URL.format(chat_oid=chat_oid),
            ),
        )

        if not response.is_success:
            raise GetChatInfoRequestError(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )

        json_data = response.json()
        return convert_chat_response_to_chat_dto(chat_data=json_data)

    async def send_message_to_chat(self, chat_oid: str, text: str) -> None:
        response = await self.http_client.post(
            url=urljoin(
                base=self.base_url,
                url=SEND_MESSAGE_TO_CHAT_URI.format(chat_oid=chat_oid),
            ),
            json={
                "text": text,
            },
        )

        if not response.is_success:
            raise SendMessageToChatRequestError(
                status_code=response.status_code,
                response_content=response.content.decode(),
            )
