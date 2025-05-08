from aiogram.filters import BaseFilter
from aiogram.types import Message


class ThreadFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (
            message.is_topic_message
            and message.message_thread_id is not None
            and message.message_thread_id != 0
        )
