from host_discovery.factory import get_config, CONFIG_FILE
from host_discovery.routers.broker.hosts import add_host
from lib.broker.pubsub import BrokerSubscriber


def create_broker_subscriber() -> BrokerSubscriber:
    config = get_config(CONFIG_FILE)

    broker_subscriber = BrokerSubscriber.create(config["BROKER"])
    broker_subscriber.subscribe('HostDiscovered', add_host)

    return broker_subscriber


def main():
    broker_subscriber = create_broker_subscriber()
    broker_subscriber.listen()


if __name__ == "__main__":
    main()
