from dataclasses import dataclass
from core.dtos.chats import ChatInfoDTO
from core.exceptions.chat import (
    ChatAlreadyExistsError,
    ChatIsNotExistsError,
    ChatNotFoundByTelegramIDError,
    ChatNotFoundByWebIDError,
)
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

    async def delete_chat(self, chat_info: ChatInfoDTO) -> None:
        if not await self.chat_repository.check_chat_exist(
            telegram_chat_id=chat_info.telegram_chat_id,
            web_chat_id=chat_info.web_chat_id,
        ):
            raise ChatIsNotExistsError()

        await self.chat_repository.delete_chat(
            web_chat_id=chat_info.web_chat_id,
            telegram_chat_id=chat_info.telegram_chat_id,
        )

    async def get_chat_info_by_telegram_id(self, telegram_chat_id: str) -> ChatInfoDTO:
        if not await self.chat_repository.check_chat_exist(
            telegram_chat_id=telegram_chat_id,
        ):
            raise ChatNotFoundByTelegramIDError(
                telegram_chat_id=telegram_chat_id,
            )

        return await self.chat_repository.get_by_telegram_id(
            telegram_chat_id=telegram_chat_id,
        )

    async def get_chat_info_by_web_id(self, web_chat_id: str) -> ChatInfoDTO:
        if not await self.chat_repository.check_chat_exist(
            web_chat_id=web_chat_id,
        ):
            raise ChatNotFoundByWebIDError(
                web_chat_id=web_chat_id,
            )
        return await self.chat_repository.get_by_external_id(web_chat_id=web_chat_id)
