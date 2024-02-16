import json

from host_discovery.models.host import Host
from host_discovery.service.message_bus import bus
from host_discovery.service.events import HostDiscovered


def add_host(data: dict) -> None:
    host = Host(**data)

    bus.handle_event(HostDiscovered(host))
