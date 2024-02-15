from fastapi import APIRouter

from host_discovery.models.host import Host
from host_discovery.service.message_bus import create_message_bus
from host_discovery.service.events import HostDiscovered

router = APIRouter()


@router.post("/hosts")
async def add_host(host: Host):

    bus = create_message_bus()
    bus.handle_event(HostDiscovered(host=host))

    return host
