import logging

import betterlogging
from aiogram import Bot, Dispatcher

from core.containers.factories import get_container
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

    async with container() as request_container:
        bot = await request_container.get(Bot)
        dp = Dispatcher()
        register_routers(dp)
        await dp.start_polling(bot)
