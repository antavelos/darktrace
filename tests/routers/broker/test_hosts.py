import logging
from typing import Callable
from unittest import mock

import pytest
from pkg_resources import resource_filename
from tinydb import Query

from host_discovery.entry.broker_listener import register_subscriptions, create_app as create_broker_listener_app
from lib.broker.pubsub import BrokerSubscriber
from lib.dns.dns import DNSClient


def make_listen_method(message: dict) -> Callable:
    def listen():
        yield message
    return listen


def create_app(expected_message: dict) -> BrokerSubscriber:
    mock_pubsub = mock.Mock()
    mock_pubsub.listen = make_listen_method(expected_message)
    mock_pubsub.subscribe = mock.Mock()

    config_file = resource_filename(__name__, "../../test_config.yml")
    app = create_broker_listener_app(config_file)
    app.pubsub = mock_pubsub

    register_subscriptions(app)

    return app


@pytest.mark.parametrize("irrelevant_message", [
    (
        {"channel": "Irrelevant", "data": {}}
    )
])
@mock.patch("host_discovery.routers.broker.hosts.add_host")
def test_add_host__irrelevant_topic__no_handler_is_called(mock_add_host, irrelevant_message):
    app = create_app(irrelevant_message)
    app.run()

    mock_add_host.assert_not_called()


@pytest.mark.parametrize("invalid_message", [
    (
        {
            "channel": "HostDiscovered",
            "data": {
                "hostname": "www.darktrace.com",
                "source": 1
            }
        }
    ),
    (
        {
            "channel": "HostDiscovered",
            "data": {
                "hostname": "www.darktrace.com",
                "invalid": "source"
            }
        }
    )
])
def test_add_host__invalid_message_data__error_is_logged(invalid_message, caplog):
    caplog.set_level(logging.ERROR)
    app = create_app(invalid_message)
    app.run()
    assert len(caplog.records) == 1


@mock.patch.object(DNSClient, "lookup")
@mock.patch("host_discovery.service.broker_publisher.publish_dns_record")
@mock.patch("host_discovery.connectors.get_tinydb")
def test_add_host__no_errors__event_handlers_are_called_properly(
        mock_tinydb,
        mock_publish_dns_record,
        mock_dns_lookup,
        test_db
):
    mock_tinydb.return_value = test_db

    message = {
        "channel": "HostDiscovered",
        "data": {
            "hostname": "www.darktrace.com",
            "source": "Datafeed"
        }
    }

    mock_dns_record = mock.Mock()
    mock_dns_lookup.return_value = mock_dns_record

    app = create_app(message)
    app.run()

    host_query = Query()
    hosts = test_db.search(host_query.hostname == message["data"]["hostname"])
    assert len(hosts) == 1

    mock_publish_dns_record.assert_called_once_with(mock_dns_record)
