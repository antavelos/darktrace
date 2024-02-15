import yaml
from pkg_resources import resource_filename

from lib.broker.pubsub import PubSub
from lib.dns.dns import DNSClient


CONFIG_FILE = resource_filename(__name__, 'config.yml')


def get_config(filename: str) -> dict:
    with open(filename, "r") as f:
        config = yaml.safe_load(f)
        if config is None:
            config = {}

    return config


def create_pubsub() -> PubSub:

    config = get_config(CONFIG_FILE)

    return PubSub.create(config["BROKER"])


def create_dns_client() -> DNSClient:
    config = get_config(CONFIG_FILE)

    return DNSClient.create(config["DNS_SERVER"])


dns_client = create_dns_client()
pubsub = create_pubsub()
