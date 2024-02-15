from typing import Type, Callable

import host_discovery.repos.hosts as hosts_repo
from host_discovery.factory import create_dns_client, create_broker_publisher
from host_discovery.service.events import HostDiscovered, Event

_dns_client = create_dns_client()
_broker_publisher = create_broker_publisher()


def handle_discovered_host(event: HostDiscovered):

    hosts_repo.store_host(event.host)

    dns_record = _dns_client.lookup(event.host.hostname)

    if dns_record is not None:
        _broker_publisher.publish('DNSRecordDiscovered', dns_record.model_dump_json())


SERVICE_EVENT_HANDLERS: dict[Type[Event], list[Callable]] = {
    HostDiscovered: [handle_discovered_host],
}
