from typing import Type, Callable

from host_discovery.repos.hosts import HostRepo
from host_discovery.factory import get_dns_client
from host_discovery.pubsub import publisher
from host_discovery.service.events import HostDiscovered, Event

_dns_client = get_dns_client()


def store_host(event: HostDiscovered):
    host_repo = HostRepo()
    host_repo.save_host(event.host)


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
