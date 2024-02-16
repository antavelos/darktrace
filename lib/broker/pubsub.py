import logging
from typing import Self, Callable

import redis

_logger = logging.getLogger(__name__)


class BrokerSubscriber:
    def __init__(self, pubsub: redis.client.PubSub):
        self.pubsub = pubsub
        self._message_handlers: dict[str, Callable] = {}

    @classmethod
    def create(cls, config: dict) -> Self:
        broker = redis.Redis(**config)
        return cls(broker.pubsub())

    def run(self):

        for message in self.pubsub.listen():
            topic = message["channel"]
            event_handler = self._message_handlers.get(topic)

            if not event_handler:
                continue

            try:
                event_handler(message["data"])
            except Exception as e:
                _logger.error(f"Error while handling {topic}: {e}")

    def subscribe(self, topic: str, message_handler: Callable):
        self._message_handlers[topic] = message_handler
        self.pubsub.subscribe(topic)


class BrokerPublisher:
    def __init__(self, broker: redis.Redis):
        self._broker = broker

    @classmethod
    def create(cls, config: dict) -> Self:
        broker = redis.Redis(**config)
        return cls(broker)

    def publish(self, topic: str, message: str):
        self._broker.publish(topic, message)
