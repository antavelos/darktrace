
from host_discovery.factory import pubsub
from host_discovery.models.host import Host
from host_discovery.service import bus
from host_discovery.service.events import HostDiscovered


def handle_host_discovered(data: dict) -> None:
    bus.handle_event(HostDiscovered(Host(**data)))


BROKER_EVENT_HANDLERS = {
    "HostDiscovered": handle_host_discovered
}


def main():

    for event in BROKER_EVENT_HANDLERS.keys():
        pubsub.subscribe(event)

    for message in pubsub.listen():
        event_handler = BROKER_EVENT_HANDLERS.get(message["channel"])
        if event_handler:
            event_handler(message["data"])
