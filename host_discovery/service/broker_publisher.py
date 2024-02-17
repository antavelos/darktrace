from host_discovery.connectors import get_broker_publisher
from lib.dns.models import DNSRecord

broker_publisher = get_broker_publisher()


def publish_dns_record(dns_record: DNSRecord):
    broker_publisher.publish("DNSRecordDiscovered", dns_record.model_dump_json())
