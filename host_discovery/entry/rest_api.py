from fastapi import FastAPI

from host_discovery.routers.http import hosts


def create_app() -> FastAPI:
    fast_api = FastAPI(title="Host Discovery")
    fast_api.include_router(hosts.router)

    return fast_api


app = create_app()
