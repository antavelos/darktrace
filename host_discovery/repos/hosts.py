import logging

from host_discovery.models.host import Host
from host_discovery.repos import STORE


_logging = logging.getLogger(__name__)


def store_host(host: Host):
    _logging.info(f"storing host: {host}")
    STORE["hosts"].append(host.dict())
    _logging.info(f"STORE: {STORE}")
