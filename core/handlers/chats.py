from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReactionTypeEmoji

from core.containers.factories import get_container
from core.exceptions.base import ApplicationException
from core.exceptions.chat import BaseWebException
from core.handlers.filters import ThreadFilter
from core.services.chats import ChatsService
from core.services.web import BaseChatWebService


router = Router()


@router.message(Command("close_chat"), ThreadFilter())
async def close_chat_and_delete_handler(message: Message):
    container = get_container()

    async with container() as request_container:
        web_servise: BaseChatWebService = await request_container.get(
            BaseChatWebService,
        )
        service: ChatsService = await request_container.get(ChatsService)

        try:
            chat_info = await service.get_chat_info_by_telegram_id(
                telegram_chat_id=message.message_thread_id,
            )

            await web_servise.delete_chat(chat_oid=chat_info.web_chat_id)
        except BaseWebException as error:
            await message.answer(
                text=error.error_text,
            )
        except ApplicationException as error:
            await message.answer(
                text=error.message,
            )


@router.message(Command("help"))
async def help_command(message: Message):
    help_text = """Available commands:
/help - Show this help message.
/close_chat - Close the current chat when the issue is resolved.
"""

    await message.answer(text=help_text)


@router.message(F.text.startswith("/"))
async def unknown_command(message: Message):
    await message.answer(
        text="Unknown command. Please use /help to see available commands.",
    )


@router.message(ThreadFilter())
async def handle_thread_message(message: Message):
    if message.text is None:
        return

    if message.from_user and message.from_user.id == message.bot.id:
        return

    container = get_container()

    async with container() as request_container:
        web_service = await request_container.get(BaseChatWebService)
        servise = await request_container.get(ChatsService)

        try:
            chat_info = await servise.get_chat_info_by_telegram_id(
                message.message_thread_id,
            )

            await web_service.send_message_to_chat(
                chat_oid=chat_info.web_chat_id,
                text=message.text,
                source="telegram",
            )
            await message.react([ReactionTypeEmoji(emoji="👍")])

        except BaseWebException as error:
            await message.answer(
                text=error.error_text,
            )

        except ApplicationException as error:
            await message.answer(
                text=error.message,
            )
