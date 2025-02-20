from aiogram import Dispatcher
from core.handlers.start import router as start_router
from core.handlers.chats import router as chats_router


def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(chats_router)
