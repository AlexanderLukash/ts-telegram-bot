from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.containers.factories import get_container
from core.handlers.converters.chats import convert_chat_dtos_to_message
from core.services.web import BaseChatWebService

router = Router()


@router.message(Command("chats"))
async def get_all_chats_handler(message: Message):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        chats = await service.get_all_chats()

    await message.answer(
        text=convert_chat_dtos_to_message(chats=chats),
    )
