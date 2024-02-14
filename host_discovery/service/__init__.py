from host_discovery.service import handlers
from host_discovery.service.message_bus import MessageBus


def _create_message_bus():
    return MessageBus(event_handlers=handlers.EVENT_HANDLERS)


bus = _create_message_bus()
