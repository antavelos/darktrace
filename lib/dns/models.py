from enum import Enum

from pydantic import BaseModel


class DNSRecordStatus(Enum):
    ACTIVE = 'A'


class DNSRecord(BaseModel):
    hostname: str
    status: DNSRecordStatus
    value: str
