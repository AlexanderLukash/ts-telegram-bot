from aiogram import Bot
from faststream import Context
from faststream.kafka import KafkaRouter

from core.consumers.schemas import NewChatMessageSchema, NewChatSchema
from core.containers.factories import get_container
from core.dtos.chats import ChatInfoDTO
from core.exceptions.base import ApplicationException
from core.exceptions.chat import BaseWebException
from core.services.chats import ChatsService
from core.services.web import BaseChatWebService
from core.settings.config import get_config

config = get_config()
router = KafkaRouter()


@router.subscriber(config.NEW_MESSAGE_TOPIC, group_id=config.KAFKA_GROUP_ID)
async def new_message_subscription_handler(
    message: NewChatMessageSchema,
    key: bytes = Context("message.raw_message.key"),
):
    if message.source == "telegram":
        return

    container = get_container()

    async with container() as request_container:
        chat_oid = key.decode()
        chat_service = await request_container.get(ChatsService)
        bot = await request_container.get(Bot)

        try:
            chat_info = await chat_service.get_chat_info_by_web_id(chat_oid)

            await bot.send_message(
                chat_id=config.TELEGRAM_GROUP_ID,
                message_thread_id=chat_info.telegram_chat_id,
                text=f"<b>{message.message_text}</b>",
            )

            await bot.session.close()

        except BaseWebException as error:
            await bot.send_message(
                chat_id=config.TELEGRAM_GROUP_ID,
                text=error.error_text,
            )

        except ApplicationException as error:
            await bot.send_message(
                chat_id=config.TELEGRAM_GROUP_ID,
                text=error.message,
            )


@router.subscriber(config.DELETE_CHAT_TOPIC, group_id=config.KAFKA_GROUP_ID)
async def delete_chat_subscription_handler(
    key: bytes = Context("message.raw_message.key"),
):
    container = get_container()

    async with container() as request_container:
        chat_oid = key.decode()
        chat_service = await request_container.get(ChatsService)
        bot = await request_container.get(Bot)
        try:
            chat_info = await chat_service.get_chat_info_by_web_id(chat_oid)

            await bot.send_message(
                chat_id=config.TELEGRAM_GROUP_ID,
                message_thread_id=chat_info.telegram_chat_id,
                text="Chat deleted.",
            )

            await bot.delete_forum_topic(
                chat_id=config.TELEGRAM_GROUP_ID,
                message_thread_id=chat_info.telegram_chat_id,
            )

            await chat_service.delete_chat(chat_info=chat_info)

            await bot.session.close()

        except BaseWebException as error:
            await bot.send_message(
                chat_id=config.TELEGRAM_GROUP_ID,
                text=error.error_text,
            )

        except ApplicationException as error:
            await bot.send_message(
                chat_id=config.TELEGRAM_GROUP_ID,
                text=error.message,
            )


@router.subscriber(config.NEW_CHAT_TOPIC, group_id=config.KAFKA_GROUP_ID)
async def new_chat_subscription_handler(
    message: NewChatSchema,
):
    container = get_container()
    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        chat_service = await request_container.get(ChatsService)
        bot = await request_container.get(Bot)
        try:
            chat_info = await service.get_chat_info(chat_oid=message.chat_oid)

            topic = await bot.create_forum_topic(
                chat_id=config.TELEGRAM_GROUP_ID,
                name=chat_info.title,
            )

            await chat_service.add_chat(
                ChatInfoDTO(
                    web_chat_id=message.chat_oid,
                    telegram_chat_id=topic.message_thread_id,
                ),
            )

            await bot.send_message(
                chat_id=config.TELEGRAM_GROUP_ID,
                message_thread_id=topic.message_thread_id,
                text=config.GREETING_TEXT.format(problem=chat_info.title),
            )

        except BaseWebException as error:
            await bot.send_message(
                chat_id=config.TELEGRAM_GROUP_ID,
                text=error.error_text,
            )

        except ApplicationException as error:
            await message.answer(
                chat_id=config.TELEGRAM_GROUP_ID,
                text=error.message,
            )
