from fastapi import FastAPI
from host_discovery.routers import hosts

app = FastAPI(title="Host Discovery")
app.include_router(hosts.router)
