from pkg_resources import resource_filename

from host_discovery.factory import get_config
import host_discovery.routers.broker.hosts as host_routers
from lib.broker.pubsub import BrokerSubscriber


def register_subscriptions(app: BrokerSubscriber):
    app.subscribe("HostDiscovered", host_routers.add_host)


def create_app(config_file: str) -> BrokerSubscriber:

    config = get_config(config_file)

    subscriber = BrokerSubscriber.create(config["BROKER"])

    return subscriber


def main():
    config_file = resource_filename(__name__, "../config.yml")
    subscriber_app = create_app(config_file)
    register_subscriptions(subscriber_app)

    subscriber_app.run()


if __name__ == "__main__":
    main()
