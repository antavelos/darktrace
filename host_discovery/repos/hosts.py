
from host_discovery.models.host import Host
from host_discovery.repos import STORE


def store_host(host: Host):
    STORE["hosts"].append(host.dict())
