import host_discovery.repos.hosts as hosts_repo
from host_discovery.service.events import HostDiscovered


def handle_discovered_host(event: HostDiscovered):

    hosts_repo.store_host(event.host)

    # lookup dns

    # publish event


EVENT_HANDLERS = {
    HostDiscovered: [handle_discovered_host],
}
