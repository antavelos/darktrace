import uvicorn
from fastapi import FastAPI

from host_discovery.routers.http import hosts


def create_app() -> FastAPI:
    fast_api = FastAPI(title="Host Discovery")
    fast_api.include_router(hosts.router)

    return fast_api


app = create_app()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
