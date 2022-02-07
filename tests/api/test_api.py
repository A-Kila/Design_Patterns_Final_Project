import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from requests import Response

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

    assert response.status_code == status.HTTP_200_OK
    assert "api_key" in response.json().keys()


def test_create_wallet(test_client: TestClient) -> None:
    user_create_response = test_client.post("/users")

    user_key: str = user_create_response.json()["api_key"]

    wallet_create_response = test_client.post("/wallets?api_key={}".format(user_key))

    assert wallet_create_response.status_code == status.HTTP_200_OK
    assert wallet_create_response.json()["balance_btc"] == 1

    for i in range(MAX_WALLET_COUNT - 1):
        test_client.post("/wallets?api_key={}".format(user_key))

    assert (
        test_client.post("/wallets?api_key={}".format(user_key)).status_code
        == status.HTTP_400_BAD_REQUEST
    )


def test_get_wallet(test_client: TestClient) -> None:
    user_create_response = test_client.post("/users")

    user_key: str = user_create_response.json()["api_key"]

    wallet_create_response = test_client.post("/wallets?api_key={}".format(user_key))

    wallet_address_first: str = wallet_create_response.json()["wallet_address"]

    wallet_get_response_first = test_client.get(
        "/wallet/{}?api_key={}".format(wallet_address_first, user_key)
    )

    assert wallet_get_response_first.status_code == status.HTTP_200_OK
    assert wallet_get_response_first.json()["balance_btc"] == 1
    assert wallet_get_response_first.json()["wallet_address"] == wallet_address_first

    if MAX_WALLET_COUNT > 1:
        wallet_address_second: str = test_client.post(
            "/wallets?api_key={}".format(user_key)
        ).json()["wallet_address"]

        wallet_get_response_second = test_client.get(
            "/wallet/{}?api_key={}".format(wallet_address_second, user_key)
        )

        assert wallet_get_response_second.status_code == status.HTTP_200_OK
        assert wallet_get_response_second.json()["balance_btc"] == 1
        assert (
            wallet_get_response_second.json()["wallet_address"] == wallet_address_second
        )

    wallet_incorrect_api_key = test_client.get(
        "/wallet/{}?api_key={}".format(wallet_address_first, "")
    )

    assert wallet_incorrect_api_key.status_code == status.HTTP_401_UNAUTHORIZED

    wallet_incorrect_address = test_client.get(
        "/wallet/{}?api_key={}".format("", user_key)
    )

    assert wallet_incorrect_address.status_code == status.HTTP_404_NOT_FOUND

    user_key_two = test_client.post("/users").json()["api_key"]

    user_two_wallet = test_client.post(
        "/wallets?api_key={}".format(user_key_two)
    ).json()["wallet_address"]

    wallet_not_your_wallet_first = test_client.get(
        "/wallet/{}?api_key={}".format(user_two_wallet, user_key)
    )

    assert wallet_not_your_wallet_first.status_code == status.HTTP_403_FORBIDDEN

    wallet_not_your_wallet_second = test_client.get(
        "/wallet/{}?api_key={}".format(wallet_address_first, user_key_two)
    )

    assert wallet_not_your_wallet_second.status_code == status.HTTP_403_FORBIDDEN


"""
get_statistics - /transactions, 
get_wallet_transactions - /wallet/{address}/transactions, 
get_transactions - /transactions, 
perform_transaction - /transaction
"""

"""api_key: str
    wallet_from: str
    wallet_to: str
    amount: float"""


def test_perform_transaction(test_client: TestClient) -> None:
    response: Response = test_client.post(
        "/transaction?api_key=user1&wallet_from=user1w1&wallet_to=user2w2&amount=1.0"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_transactions(test_client: TestClient) -> None:
    register_response: Response = test_client.post(f"/users")
    registered_user: str = register_response.json()["api_key"]
    bad_user: str = "bad_user"

    assert register_response.status_code == status.HTTP_200_OK
    good_response: Response = test_client.get(
        f"/transactions?api_key={registered_user}"
    )
    assert good_response.status_code == status.HTTP_200_OK
    assert good_response.json() == {"transactions": []}
    bad_response: Response = test_client.get(f"/transactions?api_key={bad_user}")
    # assert bad_response.status_code == 404
    # assert bad_response.json() == {'detail': "User not registered"}


def test_get_wallet_transactions(test_client: TestClient) -> None:
    pass


def test_get_statistics(test_client: TestClient) -> None:
    admin_key: str = "admin123"
    user_key: str = "not_an_admin"
    good_response: Response = test_client.get(f"/statistics?admin_key={admin_key}")
    assert good_response.status_code == status.HTTP_200_OK
    assert good_response.json() == {"number_of_transactions": 0, "platform_profit": 0.0}
    bad_response: Response = test_client.get(f"/statistics?admin_key={user_key}")
    assert bad_response.status_code == status.HTTP_403_FORBIDDEN
    assert bad_response.json() == {"detail": "Access Denied"}
