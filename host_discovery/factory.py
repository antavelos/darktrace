import yaml
from pkg_resources import resource_filename

from lib.broker.pubsub import BrokerPublisher
from lib.dns.dns import DNSClient


CONFIG_FILE = resource_filename(__name__, 'config.yml')

_dns_client = None
_broker_publisher = None


def get_config(filename: str) -> dict:
    with open(filename, "r") as f:
        config = yaml.safe_load(f)
        if config is None:
            config = {}

    return config


def create_broker_publisher() -> BrokerPublisher:
    global _broker_publisher
    if _broker_publisher is None:
        config = get_config(CONFIG_FILE)

        _broker_publisher = BrokerPublisher.create(config["BROKER"])

    return _broker_publisher


def create_dns_client() -> DNSClient:
    global _dns_client
    if _dns_client is None:
        config = get_config(CONFIG_FILE)

        _dns_client = DNSClient.create(config["DNS_SERVER"])

    return _dns_client
