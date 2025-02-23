from faststream import FastStream
from faststream.kafka.broker import KafkaBroker

from core.consumers.handlers import router
from core.settings.config import get_config


def get_app():
    config = get_config()
    broker = KafkaBroker(config.KAFKA_BROKER_URL)
    broker.include_router(router=router)

    return FastStream(broker=broker)
