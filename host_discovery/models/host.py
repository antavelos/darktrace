from pydantic import BaseModel


class Host(BaseModel):
    hostname: str
    source: str
