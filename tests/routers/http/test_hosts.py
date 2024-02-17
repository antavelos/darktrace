from unittest import mock

import pytest
from fastapi.testclient import TestClient
from tinydb import Query

from host_discovery.entry.rest_api import app
from lib.dns.dns import DNSClient

URL = "/hosts"

client = TestClient(app)


@pytest.mark.parametrize("invalid_url, expected_status_code, expected_message", [
    ("invalid", 404, "Not Found")
])
def test_add_host__invalid_url__returns_404(
        invalid_url,
        expected_status_code,
        expected_message
):
    response = client.post(invalid_url, json={})

    assert response.status_code == expected_status_code

    response_json = response.json()
    assert response_json["detail"] == expected_message


@pytest.mark.parametrize("invalid_payload, expected_field_loc, expected_message", [
    (
        {
            "hostname": "www.darktrace.com",
            "source": 1
        },
        ["body", "source"],
        "Input should be a valid string"
    ),
    (
        {
            "hostname": "www.darktrace.com",
            "invalid": "source"
        },
        ["body", "source"],
        "Field required"
    )
])
@pytest.mark.parametrize("expected_status_code", [422])
def test_add_host__invalid_payload__returns_422(
        invalid_payload,
        expected_field_loc,
        expected_message,
        expected_status_code
):
    response = client.post(URL, json=invalid_payload)

    assert response.status_code == expected_status_code

    response_json = response.json()
    assert response_json["detail"][0]["loc"] == expected_field_loc
    assert response_json["detail"][0]["msg"] == expected_message


@mock.patch.object(DNSClient, "lookup")
@mock.patch("host_discovery.service.broker_publisher.publish_dns_record")
@mock.patch("host_discovery.connectors.get_tinydb")
def test_add_host__no_errors__event_handlers_are_called_properly__returns_201(
        mock_tinydb,
        mock_publish_dns_record,
        mock_dns_lookup,
        test_db
):
    mock_tinydb.return_value = test_db

    payload = {
        "hostname": "www.darktrace.com",
        "source": "Datafeed"
    }
    mock_dns_record = mock.Mock()
    mock_dns_lookup.return_value = mock_dns_record

    response = client.post(URL, json=payload)

    assert response.status_code == 201

    host_query = Query()
    hosts = test_db.search(host_query.hostname == payload["hostname"])
    assert len(hosts) == 1

    mock_publish_dns_record.assert_called_once_with(mock_dns_record)
