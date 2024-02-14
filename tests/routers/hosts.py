import pytest
from fastapi.testclient import TestClient
from host_discovery.app import app

URL = '/hosts'

client = TestClient(app)


@pytest.mark.parametrize('invalid_url, expected_status_code, expected_message', [
    ('invalid', 404, 'Not Found')
])
def test_add_hosts__invalid_url__returns_404(
        invalid_url,
        expected_status_code,
        expected_message
):
    response = client.post(invalid_url, json={})

    assert response.status_code == expected_status_code

    response_json = response.json()
    assert response_json['detail'] == expected_message


@pytest.mark.parametrize('invalid_payload, expected_field_loc, expected_message', [
    (
        {
            "hostname": "www.darktrace.com",
            "source": 1
        },
        ['body', 'source'],
        'Input should be a valid string'
    ),
    (
        {
            "hostname": "www.darktrace.com",
            "invalid": "source"
        },
        ['body', 'source'],
        'Field required'
    )
])
@pytest.mark.parametrize('expected_status_code', [422])
def test_add_hosts__invalid_payload__returns_422(
        invalid_payload,
        expected_field_loc,
        expected_message,
        expected_status_code
):
    response = client.post(URL, json=invalid_payload)

    assert response.status_code == expected_status_code

    response_json = response.json()
    assert response_json['detail'][0]['loc'] == expected_field_loc
    assert response_json['detail'][0]['msg'] == expected_message
