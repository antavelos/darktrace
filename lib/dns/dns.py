from requests import Session

from lib.dns.models import DNSRecordStatus, DNSRecord


class DNSClient:
    _BASE_URL_FORMAT = "{scheme}://{host}/dns-service/"

    def __init__(self, config: dict) -> None:

        self.session = Session()
        self.session.auth = config.get("auth")
        self.session.verify = config.get("verify", False)

        self._base_url = DNSClient._BASE_URL_FORMAT.format(scheme=config["scheme"], host=config["host"])

        self._url_hosts_by_hostname = self._base_url + "hosts/{hostname}"

    def lookup(self, hostname: str, status=DNSRecordStatus.ACTIVE) -> DNSRecord | None:
        """
            Calls the http://dns-service/hosts/{hostname} endpoint of the corresponding DNS service and returns the
            DNS record if found.
        """
        url = self._url_hosts_by_hostname.format(hostname=hostname)

        response = self.session.get(url, params={"status": status.value})

        if response.content == 0:
            return None

        return DNSRecord(**response.json())
