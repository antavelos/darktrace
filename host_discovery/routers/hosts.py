from fastapi import APIRouter

from host_discovery.models.host import Host
from host_discovery.service import bus
from host_discovery.service.events import HostDiscovered

router = APIRouter()


@router.post("/hosts")
async def add_host(host: Host):

    bus.handle_event(HostDiscovered(host=host))

    return host
