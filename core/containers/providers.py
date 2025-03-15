from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dishka import Provider, Scope, provide
from httpx import AsyncClient

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
    ) -> BaseChatWebService:
        return ChatWebService(
            http_client=http_client,
            base_url=config.WEB_API_BASE_URL,
        )

    @provide(scope=Scope.APP)
    def get_telegram_bot(self, config: Config) -> Bot:
        return Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML"),
        )
