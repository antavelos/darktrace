from dataclasses import dataclass
from enum import Enum


class DNSRecordStatus(Enum):
    ACTIVE = 'A'


@dataclass
class DNSRecord:
    hostname: str
    status: DNSRecordStatus
    value: str
