import http

from fastapi.testclient import TestClient

from anv import main

client = TestClient(main.app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == http.HTTPStatus.OK


def test_resync_contract_token_id():
    chain = "binance"
    contract_address = "0x1ddb2c0897daf18632662e71fdd2dbdc0eb3a9ec"
    token_id = "100300679127"
    response = client.get(
        f"/v1/nfts/{chain}/{contract_address}/{token_id}?resync=false"
    )
    assert response.status_code == http.HTTPStatus.OK


def test_resync_contract_invalid_token_id():
    chain = "binance"
    contract_address = "0x1ddb2c0897daf18632662e71fdd2dbdc0eb3a9ec"
    token_id = "1234567890"
    response = client.get(
        f"/v1/nfts/{chain}/{contract_address}/{token_id}?resync=false"
    )
    assert response.status_code == http.HTTPStatus.NOT_FOUND
