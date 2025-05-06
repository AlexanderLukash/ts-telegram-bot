from abc import ABC, abstractmethod

from aiosqlite import connect
from attr import dataclass

from core.dtos.chats import ChatInfoDTO
from core.exceptions.chat import CharInfoNotFoundError
from core.repositories.sqls import (
    ADD_NEW_CHAT_INFO,
    GET_CHAT_INFO_BY_TELEGRAM_ID,
    GET_CHAT_INFO_BY_WEB_ID,
    GET_CHATS_COUNT,
)


@dataclass(eq=False)
class BaseChatRepository(ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_chat_id: int) -> ChatInfoDTO: ...

    @abstractmethod
    async def get_by_external_id(self, web_chat_id: str) -> ChatInfoDTO: ...

    @abstractmethod
    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO: ...

    @abstractmethod
    async def check_chat_exist(
        self,
        web_chat_id: str | None,
        telegram_chat_id: str | None,
    ) -> bool: ...


@dataclass(eq=False)
class SQLChatRepository(BaseChatRepository):
    database_url: str

    async def get_by_telegram_id(self, telegram_chat_id: int) -> ChatInfoDTO:
        async with connect(self.database_url) as db:
            result = await db.execute_insert(
                GET_CHAT_INFO_BY_TELEGRAM_ID,
                (telegram_chat_id,),
            )

            if result is None:
                raise CharInfoNotFoundError(telegram_chat_id=telegram_chat_id)

            return ChatInfoDTO(
                web_chat_id=result[0],
                telegram_chat_id=result[1],
            )

    async def get_by_external_id(self, web_chat_id: str) -> ChatInfoDTO:
        async with connect(self.database_url) as db:
            result = await db.execute_insert(
                GET_CHAT_INFO_BY_WEB_ID,
                (web_chat_id,),
            )

            if result is None:
                raise CharInfoNotFoundError(web_chat_id=web_chat_id)

            return ChatInfoDTO(
                web_chat_id=result[0],
                telegram_chat_id=result[1],
            )

    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        async with connect(self.database_url) as db:
            await db.execute_insert(
                ADD_NEW_CHAT_INFO,
                (chat_info.web_chat_id, chat_info.telegram_chat_id),
            )
            await db.commit()

            return ChatInfoDTO(
                web_chat_id=chat_info.web_chat_id,
                telegram_chat_id=chat_info.telegram_chat_id,
            )

    async def check_chat_exist(
        self,
        web_chat_id: str | None,
        telegram_chat_id: str | None,
    ) -> bool:
        async with connect(self.database_url) as db:
            result = await db.execute_insert(
                GET_CHATS_COUNT,
                (web_chat_id, telegram_chat_id),
            )

            if result is None:
                raise False

            return result[0] > 0
