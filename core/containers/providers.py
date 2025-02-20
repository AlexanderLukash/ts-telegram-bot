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
    def get_chats_web_service(self) -> BaseChatWebService:
        return ChatWebService(
            http_client=self.get_http_client(),
            base_url=self.get_config().WEB_API_BASE_URL,
        )
