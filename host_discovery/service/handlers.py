from typing import Type, Callable

import host_discovery.repos.hosts as hosts_repo
from host_discovery.factory import create_dns_client
from host_discovery.pubsub.publisher import publish_dns_record
from host_discovery.service.events import HostDiscovered, Event

_dns_client = create_dns_client()


def handle_discovered_host(event: HostDiscovered):

    hosts_repo.store_host(event.host)

    dns_record = _dns_client.lookup(event.host.hostname)

    if dns_record is not None:
        publish_dns_record(dns_record)


SERVICE_EVENT_HANDLERS: dict[Type[Event], list[Callable]] = {
    HostDiscovered: [handle_discovered_host],
}
