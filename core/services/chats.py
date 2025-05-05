from dataclasses import dataclass
from core.dtos.chats import ChatInfoDTO
from core.repositories.chats.base import BaseChatRepository


@dataclass(eq=True)
class ChatsService:
    chat_repository: BaseChatRepository

    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        # TODO: check if chat already exists
        return await self.chat_repository.add_chat(chat_info)
