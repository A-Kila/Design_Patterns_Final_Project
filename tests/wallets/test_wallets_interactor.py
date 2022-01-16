import pytest

from app.core.wallets.wallets_interactor import (
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
