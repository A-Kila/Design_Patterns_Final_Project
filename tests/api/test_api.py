import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from app.core.facade import WalletService
from app.infra.fastapi.api import wallet_api
from app.infra.in_memory.transactions_repository import TransactionRepositoryInMemory
from app.infra.in_memory.user_in_memory import UserInMemoryRepository
from app.infra.in_memory.wallet_repository import InMemoryWalletRepository
from definitions import MAX_WALLET_COUNT


@pytest.fixture()
def test_client() -> TestClient:
    app = FastAPI()

    app.include_router(wallet_api)
    app.state.core = WalletService.create(
        UserInMemoryRepository(),
        InMemoryWalletRepository(),
        TransactionRepositoryInMemory(),
    )

    return TestClient(app)


def test_register_user(test_client: TestClient) -> None:
    response = test_client.post("/users")

    assert response.status_code == 200
    assert "api_key" in response.json().keys()


def test_create_wallet(test_client: TestClient):
    user_create_response = test_client.post("/users")

    user_key: str = user_create_response.json()["api_key"]

    wallet_create_response = test_client.post("/wallets?api_key={}".format(user_key))

    assert wallet_create_response.status_code == 200
    assert wallet_create_response.json()["balance_btc"] == 1

    for i in range(MAX_WALLET_COUNT - 1):
        test_client.post("/wallets?api_key={}".format(user_key))

    assert test_client.post("/wallets?api_key={}".format(user_key)).status_code == 400


def test_get_wallet(test_client: TestClient) -> None:
    user_create_response = test_client.post("/users")

    user_key: str = user_create_response.json()["api_key"]

    wallet_create_response = test_client.post("/wallets?api_key={}".format(user_key))

    wallet_address_first: str = wallet_create_response.json()["wallet_address"]

    wallet_get_response_first = test_client.get(
        "/wallet/{}?api_key={}".format(wallet_address_first, user_key)
    )

    assert wallet_get_response_first.status_code == 200
    assert wallet_get_response_first.json()["balance_btc"] == 1
    assert wallet_get_response_first.json()["wallet_address"] == wallet_address_first

    if MAX_WALLET_COUNT > 1:
        wallet_address_second: str = test_client.post(
            "/wallets?api_key={}".format(user_key)
        ).json()["wallet_address"]

        wallet_get_response_second = test_client.get(
            "/wallet/{}?api_key={}".format(wallet_address_second, user_key)
        )

        assert wallet_get_response_second.status_code == 200
        assert wallet_get_response_second.json()["balance_btc"] == 1
        assert (
            wallet_get_response_second.json()["wallet_address"] == wallet_address_second
        )

    wallet_incorrect_api_key = test_client.get(
        "/wallet/{}?api_key={}".format(wallet_address_first, "")
    )

    assert wallet_incorrect_api_key.status_code == 401

    wallet_incorrect_address = test_client.get(
        "/wallet/{}?api_key={}".format("", user_key)
    )

    assert wallet_incorrect_address.status_code == 404

    user_key_two = test_client.post("/users").json()["api_key"]

    user_two_wallet = test_client.post(
        "/wallets?api_key={}".format(user_key_two)
    ).json()["wallet_address"]

    wallet_not_your_wallet_first = test_client.get(
        "/wallet/{}?api_key={}".format(user_two_wallet, user_key)
    )

    assert wallet_not_your_wallet_first.status_code == 403

    wallet_not_your_wallet_second = test_client.get(
        "/wallet/{}?api_key={}".format(wallet_address_first, user_key_two)
    )

    assert wallet_not_your_wallet_second.status_code == 403
