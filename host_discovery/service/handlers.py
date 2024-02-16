from typing import Type, Callable

import host_discovery.repos.hosts as hosts_repo
from host_discovery.factory import create_dns_client
from host_discovery.pubsub import publisher
from host_discovery.service.events import HostDiscovered, Event

_dns_client = create_dns_client()


def store_host(event: HostDiscovered):
    hosts_repo.store_host(event.host)


def lookup_dns(event: HostDiscovered):
    dns_record = _dns_client.lookup(event.host.hostname)

    if dns_record is not None:
        publisher.publish_dns_record(dns_record)


SERVICE_EVENT_HANDLERS: dict[Type[Event], list[Callable]] = {
    HostDiscovered: [
        store_host,
        lookup_dns
    ],
}
