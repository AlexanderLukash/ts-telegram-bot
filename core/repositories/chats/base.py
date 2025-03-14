from abc import ABC, abstractmethod

from core.dtos.messages import ChatInfoDTO


class BaseChatRepository(ABC):
    @abstractmethod
    async def initialize(self): ...

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> ChatInfoDTO: ...

    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> ChatInfoDTO: ...

    @abstractmethod
    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO: ...


class SQLChatRepository(BaseChatRepository):
    async def initialize(self): ...

    async def get_by_telegram_id(self, telegram_id: int) -> ChatInfoDTO: ...

    async def get_by_external_id(self, external_id: str) -> ChatInfoDTO: ...

    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO: ...
