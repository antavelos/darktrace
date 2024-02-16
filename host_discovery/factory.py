import yaml
from pkg_resources import resource_filename
from tinydb import TinyDB

from lib.broker.pubsub import BrokerPublisher
from lib.dns.dns import DNSClient


CONFIG_FILE = resource_filename(__name__, "config.yml")

_config = None
_dns_client = None
_broker_publisher = None
_db = None


def get_config(config_file: str) -> dict:
    global _config
    if _config is None:
        with open(config_file, "r") as f:
            _config = yaml.safe_load(f)
            if _config is None:
                _config = {}

    return _config


def get_broker_publisher(config_file: str = None) -> BrokerPublisher:
    global _broker_publisher
    if _broker_publisher is None:
        config = get_config(config_file or CONFIG_FILE)

        _broker_publisher = BrokerPublisher.create(config["BROKER"])

    return _broker_publisher


def get_dns_client(config_file: str = None) -> DNSClient:
    global _dns_client
    if _dns_client is None:
        config = get_config(config_file or CONFIG_FILE)

        _dns_client = DNSClient(config["DNS_SERVER"])

    return _dns_client


def get_tinydb(config_file: str = None):
    global _db
    if _db is None:
        config = get_config(config_file or CONFIG_FILE)
        db_file = config.get("DB") or resource_filename(__name__, "../db.json")

        _db = TinyDB(db_file)
    return _db
