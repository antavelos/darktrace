from dataclasses import dataclass

from host_discovery.models.host import Host


class Event:
    ...


@dataclass
class HostDiscovered(Event):
    host: Host
