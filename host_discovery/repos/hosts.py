from host_discovery import connectors
from host_discovery.models.host import Host


class HostRepo:

    def __init__(self):
        self._db = connectors.get_tinydb()

    def save_host(self, host: Host):
        self._db.insert(host.dict())
