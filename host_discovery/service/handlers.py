from host_discovery.service.events import HostDiscovered


def handle_discovered_host(event: HostDiscovered):
    ...
    # store host

    # lookup dns

    # publish event


EVENT_HANDLERS = {
    HostDiscovered: [handle_discovered_host],
}
