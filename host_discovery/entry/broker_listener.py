from host_discovery.entry import pubsub
from host_discovery.models.host import Host
from host_discovery.service import bus
from host_discovery.service.events import HostDiscovered


def handle_host_discovered(data: dict) -> None:
    bus.handle_event(HostDiscovered(Host(**data)))


EVENT_HANDLERS = {
    "HostDiscovered": handle_host_discovered
}


def setup_subscriptions():
    for event in EVENT_HANDLERS.keys():
        pubsub.subscribe(event)


def main():
    setup_subscriptions()

    for message in pubsub.listen():
        event_handler = EVENT_HANDLERS.get(message["channel"])
        if event_handler:
            event_handler(message["data"])
