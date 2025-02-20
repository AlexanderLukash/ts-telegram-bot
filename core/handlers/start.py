from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.containers.factories import get_container
from core.settings.config import Config

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    container = get_container()

    async with container() as container:
        config = await container.get(Config)

    await message.answer(text=config.GREETING_TEXT)
