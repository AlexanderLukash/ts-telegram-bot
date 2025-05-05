from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dishka import AnyOf, Provider, Scope, provide
from httpx import AsyncClient

from core.repositories.chats.base import BaseChatRepository, SQLChatRepository
from core.services.chats import ChatsService
from core.services.web import BaseChatWebService, ChatWebService
from core.settings.config import Config


class DefaultProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config()

    @provide(scope=Scope.REQUEST)
    def get_http_client(self) -> AsyncClient:
        return AsyncClient()

    @provide(scope=Scope.REQUEST)
    def get_chats_web_service(
        self,
        config: Config,
        http_client: AsyncClient,
    ) -> AnyOf[BaseChatWebService, ChatWebService]:
        return ChatWebService(
            http_client=http_client,
            base_url=config.WEB_API_BASE_URL,
        )

    @provide(scope=Scope.REQUEST)
    def get_telegram_bot(self, config: Config) -> Bot:
        return Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML"),
        )

    @provide(scope=Scope.REQUEST)
    def get_chats_repository(
        self,
        config: Config,
    ) -> AnyOf[BaseChatRepository, SQLChatRepository]:
        return SQLChatRepository(database_url=config.DATABASE_NAME)

    @provide(scope=Scope.REQUEST)
    def get_chats_service(self, chat_repository: BaseChatRepository) -> ChatsService:
        return ChatsService(chat_repository=chat_repository)
