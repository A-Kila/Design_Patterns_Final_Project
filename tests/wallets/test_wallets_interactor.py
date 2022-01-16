import pytest

from app.core.users.users_interactor import UsersInteractor, UsersResponse
from app.core.wallets.wallets_interactor import (
    WalletGetRequest,
    WalletPostRequest,
    WalletResponse,
    WalletsInteractor,
)
from app.infra.in_memory.user_in_memory import UserInMemoryRepository
from app.infra.in_memory.wallet_repository import InMemoryWalletRepository
from app.infra.rateapi.coingecko import CoinGeckoApi


@pytest.fixture()
def wallet_interactor() -> WalletsInteractor:
    return WalletsInteractor(
        user_repo=UserInMemoryRepository(),
        wallet_repo=InMemoryWalletRepository(),
        rate_getter=CoinGeckoApi(),
    )


def test_create_wallet(wallet_interactor: WalletsInteractor):
    request = WalletPostRequest(api_key="key_1")

    response: WalletResponse = wallet_interactor.create_wallet(request=request)

    assert response.balance_btc
    assert response.balance_usd
    assert response.wallet_address


def test_create_several_wallet_success(wallet_interactor: WalletsInteractor):
    request_1 = WalletPostRequest(api_key="key_1")
    response_1: WalletResponse = wallet_interactor.create_wallet(request=request_1)

    assert response_1.balance_btc
    assert response_1.balance_usd
    assert response_1.wallet_address

    request_2 = WalletPostRequest(api_key="key_1")
    response_2: WalletResponse = wallet_interactor.create_wallet(request=request_2)

    assert response_2.balance_btc
    assert response_2.balance_usd
    assert response_2.wallet_address


def test_create_several_wallet_limit_fail(wallet_interactor: WalletsInteractor):
    request_1 = WalletPostRequest(api_key="key_1")
    response_1: WalletResponse = wallet_interactor.create_wallet(request=request_1)

    assert response_1.balance_btc
    assert response_1.balance_usd
    assert response_1.wallet_address

    request_2 = WalletPostRequest(api_key="key_2")
    response_2: WalletResponse = wallet_interactor.create_wallet(request=request_2)

    assert response_2.balance_btc
    assert response_2.balance_usd
    assert response_2.wallet_address

    request_3 = WalletPostRequest(api_key="key_3")
    response_3: WalletResponse = wallet_interactor.create_wallet(request=request_3)

    assert response_3.balance_btc
    assert response_3.balance_usd
    assert response_3.wallet_address

    request_4 = WalletPostRequest(api_key="key_4")
    with pytest.raises(Exception):
        wallet_interactor.create_wallet(request=request_4)


def test_get_wallet_success(wallet_interactor: WalletsInteractor):
    users_interactor: UsersInteractor = UsersInteractor(
        user_repo=wallet_interactor.user_repo
    )

    user: UsersResponse = users_interactor.generate_new_api_key()
    api_key: str = user.api_key

    request_create = WalletPostRequest(api_key=api_key)
    wallet: WalletResponse = wallet_interactor.create_wallet(request=request_create)

    request = WalletGetRequest(api_key=api_key, wallet_address=wallet.wallet_address)
    response: WalletResponse = wallet_interactor.get_wallet(request=request)

    assert response.wallet_address == wallet.wallet_address
    assert response.balance_btc == wallet.balance_btc
    assert response.balance_usd == wallet.balance_usd


def test_get_wallet_with_invalid_user_id(wallet_interactor: WalletsInteractor):
    request_create = WalletPostRequest(api_key="key_1")
    wallet: WalletResponse = wallet_interactor.create_wallet(request=request_create)

    request = WalletGetRequest(
        api_key="INVALID_KEY", wallet_address=wallet.wallet_address
    )
    with pytest.raises(Exception):
        wallet_interactor.get_wallet(request=request)


def test_get_wallet_with_invalid_address(wallet_interactor: WalletsInteractor):
    users_interactor: UsersInteractor = UsersInteractor(
        user_repo=wallet_interactor.user_repo
    )

    user: UsersResponse = users_interactor.generate_new_api_key()
    api_key: str = user.api_key

    request_create = WalletPostRequest(api_key=api_key)
    wallet_interactor.create_wallet(request=request_create)

    request = WalletGetRequest(api_key=api_key, wallet_address="INVALID_ADDRESS")
    with pytest.raises(Exception):
        wallet_interactor.get_wallet(request=request)
