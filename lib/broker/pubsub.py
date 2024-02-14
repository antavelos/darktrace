from typing import Self

import redis


class PubSub:

    def __init__(self, broker):
        self._broker = broker

    @classmethod
    def create(cls, config: dict) -> Self:
        broker = redis.Redis(**config)
        return PubSub(broker)

    def listen(self):
        self._broker.listen()

    def publish(self, topic: str, message: dict):
        self._broker.publish(topic, message)

    def subscribe(self, topic: str):
        self._broker.subscribe(topic)