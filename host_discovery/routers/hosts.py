from fastapi import APIRouter

from host_discovery.models.host import Host

router = APIRouter()


@router.post("/hosts")
async def add_host(host: Host):
    # store host

    # dns lookup
    # if active then publish **DNSRecordDiscovered**

    return host.json()
