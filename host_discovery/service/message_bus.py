import logging
from typing import Callable, Type

from host_discovery.service import events

_logger = logging.getLogger(__name__)


class MessageBus:

    def __init__(self, event_handlers: dict[Type[events.Event], list[Callable]]):
        self.event_handlers = event_handlers

    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                _logger.debug(f"Handling event {event} with handler {handler}")
                handler(event)
            except Exception as e:
                _logger.exception(f"Exception handling event {event}: {e}")
                continue
