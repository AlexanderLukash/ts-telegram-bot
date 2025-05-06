from dataclasses import dataclass
from core.dtos.chats import ChatInfoDTO
from core.exceptions.chat import ChatAlreadyExistsError
from core.repositories.chats.base import BaseChatRepository


@dataclass(eq=True)
class ChatsService:
    chat_repository: BaseChatRepository

    async def add_chat(self, chat_info: ChatInfoDTO) -> ChatInfoDTO:
        if await self.chat_repository.check_chat_exist(
            web_chat_id=chat_info.web_chat_id,
            telegram_chat_id=chat_info.telegram_chat_id,
        ):
            raise ChatAlreadyExistsError(
                web_chat_id=chat_info.web_chat_id,
                telegram_chat_id=chat_info.telegram_chat_id,
            )
        return await self.chat_repository.add_chat(chat_info)
