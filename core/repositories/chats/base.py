from abc import ABC, abstractmethod

from aiosqlite import connect

from core.dtos.messages import ChatInfoDTO
from core.repositories.sqls import ADD_NEW_CHAT_INFO


class BaseChatRepository(ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> ChatInfoDTO: ...

    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> ChatInfoDTO: ...

    @abstractmethod
    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO: ...


class SQLChatRepository(BaseChatRepository):
    database_url: str

    async def get_by_telegram_id(self, telegram_id: int) -> ChatInfoDTO: ...

    async def get_by_external_id(self, external_id: str) -> ChatInfoDTO: ...

    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        async with connect(self.database_url) as db:
            row = await db.execute_insert(
                ADD_NEW_CHAT_INFO,
                (chat_info.web_chat_id, chat_info.telegram_chat_id),
            )
            web_chat_id, telegram_chat_id = row

            return ChatInfoDTO(
                web_chat_id=web_chat_id,
                telegram_chat_id=telegram_chat_id,
            )
