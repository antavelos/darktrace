import host_discovery.repos.hosts as hosts_repo
from host_discovery.factory import create_dns_client, create_pubsub
from host_discovery.service.events import HostDiscovered


dns_client = create_dns_client()
pubsub = create_pubsub()


def handle_discovered_host(event: HostDiscovered):

    hosts_repo.store_host(event.host)

    # lookup dns
    dns_record = dns_client.lookup(event.host.hostname)

    if dns_record is not None:
        # publish event
        pubsub.publish('DNSRecordDiscovered', dns_record.to_json())


SERVICE_EVENT_HANDLERS = {
    HostDiscovered: [handle_discovered_host],
}
