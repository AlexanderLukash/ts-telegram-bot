from aiogram import Bot
from faststream import Context
from faststream.kafka import KafkaRouter

from core.consumers.schemas import NewChatMessageSchema
from core.containers.factories import get_container
from core.services.web import BaseChatWebService
from core.settings.config import get_config

config = get_config()
router = KafkaRouter()


@router.subscriber(config.NEW_MESSAGE_TOPIC, group_id=config.KAFKA_GROUP_ID)
async def new_message_subscription_handler(
    message: NewChatMessageSchema,
    key: bytes = Context("message.raw_message.key"),
):
    container = get_container()

    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        listeners = await service.get_chat_listeners(chat_oid=key.decode())
        print(listeners)

        bot = await request_container.get(Bot)

        for listener in listeners:
            await bot.send_message(chat_id=listener.oid, text=message.message_text)
