import pytest
from fastapi import HTTPException, status

from app.core.users.users_interactor import UsersInteractor, UsersResponse
from app.core.wallets.wallets_interactor import (
    WalletGetRequest,
    WalletPostRequest,
    WalletResponse,
    WalletsInteractor,
)
from app.infra.fastapi.exception_handler import HttpExceptionHandler
from app.infra.in_memory.user_in_memory import UserInMemoryRepository
from app.infra.in_memory.wallet_repository import InMemoryWalletRepository
from app.infra.in_memory.rate_getter_in_memory import RateGetterInMemory


@pytest.fixture()
def wallet_interactor() -> WalletsInteractor:
    return WalletsInteractor(
        user_repo=UserInMemoryRepository(),
        wallet_repo=InMemoryWalletRepository(),
        rate_getter=RateGetterInMemory(),
        exception_handler=HttpExceptionHandler(),
    )


def test_create_wallet(wallet_interactor: WalletsInteractor) -> None:
    request = WalletPostRequest(api_key="key_1")

    response: WalletResponse = wallet_interactor.create_wallet(request=request)

    assert response.balance_btc
    assert response.balance_usd
    assert response.wallet_address


def test_create_several_wallet_success(wallet_interactor: WalletsInteractor) -> None:
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


def test_create_several_wallet_limit_fail(wallet_interactor: WalletsInteractor) -> None:
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
    with pytest.raises(HTTPException) as e:
        wallet_interactor.create_wallet(request=request_4)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST


def test_get_wallet_success(wallet_interactor: WalletsInteractor) -> None:
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


def test_get_wallet_with_invalid_address(wallet_interactor: WalletsInteractor) -> None:
    users_interactor: UsersInteractor = UsersInteractor(
        user_repo=wallet_interactor.user_repo
    )

    user: UsersResponse = users_interactor.generate_new_api_key()
    api_key: str = user.api_key

    request_create = WalletPostRequest(api_key=api_key)
    wallet_interactor.create_wallet(request=request_create)

    request = WalletGetRequest(api_key=api_key, wallet_address="INVALID_ADDRESS")

    with pytest.raises(HTTPException) as e:
        wallet_interactor.get_wallet(request=request)
    assert e.value.status_code == status.HTTP_404_NOT_FOUND


def test_get_wallet_with_other_user(wallet_interactor: WalletsInteractor) -> None:
    users_interactor: UsersInteractor = UsersInteractor(
        user_repo=wallet_interactor.user_repo
    )

    user_1: UsersResponse = users_interactor.generate_new_api_key()
    user_2: UsersResponse = users_interactor.generate_new_api_key()
    api_key_1: str = user_1.api_key
    api_key_2: str = user_2.api_key

    request_create = WalletPostRequest(api_key=api_key_1)
    wallet: WalletResponse = wallet_interactor.create_wallet(request=request_create)

    request = WalletGetRequest(api_key=api_key_2, wallet_address=wallet.wallet_address)
    with pytest.raises(HTTPException) as e:
        wallet_interactor.get_wallet(request=request)
    assert e.value.status_code == status.HTTP_403_FORBIDDEN
