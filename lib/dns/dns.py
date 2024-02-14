from typing import Self

from lib.dns.base import RequestHandler
from lib.dns.models import DNSRecordStatus, DNSRecord


class DNSClient:
    _BASE_URL = 'dns-service/'

    def __init__(self, request_handler: RequestHandler) -> None:
        self._request_handler = request_handler
        self._url_hosts_by_hostname = self._BASE_URL + "hosts/{hostname}"

    @classmethod
    def create(cls, config: dict) -> Self:
        request_handler = RequestHandler(**config)

        return DNSClient(request_handler)

    def lookup(self, hostname: str, status: DNSRecordStatus = DNSRecordStatus.ACTIVE) -> DNSRecord | None:
        """
            Calls the http://dns-service/hosts/{hostname} endpoint of the corresponding DNS service and returns the
            DNS record if found.
        """
        url = self._url_hosts_by_hostname.format(hostname=hostname)

        response = self._request_handler.get(url, params={status: status})

        if response.content == 0:
            return None

        return DNSRecord(**response.json())
