import logging

import betterlogging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties


from core.containers.factories import get_container
from core.settings.config import Config
from core.setup_handlers import register_routers


def setup_logging():
    log_level = logging.INFO
    betterlogging.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def main():
    setup_logging()
    container = get_container()

    async with container() as container:
        config = await container.get(Config)
        bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML"),
        )
    dp = Dispatcher()
    register_routers(dp)
    await dp.start_polling(bot)
