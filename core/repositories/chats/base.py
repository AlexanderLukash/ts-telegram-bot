from abc import ABC, abstractmethod

from aiosqlite import connect
from attr import dataclass

from core.dtos.chats import ChatInfoDTO
from core.exceptions.chat import CharInfoNotFoundError
from core.repositories.sqls import (
    ADD_NEW_CHAT_INFO,
    DELETE_CHAT_QUERY,
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
    async def delete_chat(
        self,
        web_chat_id: str = "",
        telegram_chat_id: str = "",
    ) -> None: ...

    @abstractmethod
    async def check_chat_exist(
        self,
        web_chat_id: str | None = None,
        telegram_chat_id: str | None = None,
    ) -> bool: ...


@dataclass(eq=False)
class SQLChatRepository(BaseChatRepository):
    database_url: str

    async def get_by_telegram_id(self, telegram_chat_id: int) -> ChatInfoDTO:
        async with connect(self.database_url) as db:
            result = await db.execute_fetchall(
                GET_CHAT_INFO_BY_TELEGRAM_ID,
                (telegram_chat_id,),
            )

            if result is None:
                raise CharInfoNotFoundError(telegram_chat_id=telegram_chat_id)

            row = result[0]
            return ChatInfoDTO(
                web_chat_id=row[0],
                telegram_chat_id=row[1],
            )

    async def get_by_external_id(self, web_chat_id: str) -> ChatInfoDTO:
        async with connect(self.database_url) as db:
            result = await db.execute_fetchall(
                GET_CHAT_INFO_BY_WEB_ID,
                (web_chat_id,),
            )

            if result is None:
                raise CharInfoNotFoundError(web_chat_id == web_chat_id)

            row = result[0]
            return ChatInfoDTO(
                web_chat_id=row[0],
                telegram_chat_id=row[1],
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
        web_chat_id: str | None = None,
        telegram_chat_id: str | None = None,
    ) -> bool:
        async with connect(self.database_url) as db:
            result = await db.execute_fetchall(
                GET_CHATS_COUNT,
                (web_chat_id, telegram_chat_id),
            )

            if result is None:
                return False

            result, *_ = result

            return result[0] > 0

    async def delete_chat(
        self,
        web_chat_id: str = "",
        telegram_chat_id: str = "",
    ) -> None:
        async with connect(self.database_url) as db:
            await db.execute(
                DELETE_CHAT_QUERY,
                (web_chat_id, telegram_chat_id),
            )
            await db.commit()
