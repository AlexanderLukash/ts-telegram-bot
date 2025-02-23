from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from core.containers.factories import get_container
from core.exceptions.base import ApplicationException
from core.exceptions.chat import BaseWebException
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


@router.message(Command("set_chat"))
async def set_chat_handler(message: Message, command: CommandObject):
    container = get_container()

    chat_oid: str = command.args
    if chat_oid:
        async with container() as request_container:
            service = await request_container.get(BaseChatWebService)
        try:
            await service.add_listener(
                telegram_chat_id=message.from_user.id,
                chat_oid=chat_oid,
            )
            await message.answer(
                text=f"{message.from_user.id}, {chat_oid}",
            )
        except BaseWebException as error:
            await message.answer(
                text=error.error_text,
            )
        except ApplicationException as error:
            await message.answer(
                text=error.message,
            )

    else:
        await message.answer(
            text="Please Provide Chat Oid. For example: /set_chat 123456",
        )
