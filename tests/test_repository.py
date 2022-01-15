import pytest

from app.core.users.users_interactor import IUserRepository
from app.infra.in_memory.user_in_memory import UserInMemoryRepository
from app.infra.in_memory.wallet_repository import InMemoryWalletRepository


@pytest.fixture()
def user_repo() -> IUserRepository:
    return UserInMemoryRepository()


# @pytest.fixture()
# def wallet_repo() -> IWalletRepository: # need interface
#     return InMemoryWalletRepository()


def test_user_repository_store_get_user(user_repo: IUserRepository):
    user_repo.store_user("0imfnc8mVLWwsAawjYr4Rx")
    user_repo.store_user("1imfnc8mVLWwsAawjYr4Rx")
    assert user_repo.get_user_id("0imfnc8mVLWwsAawjYr4Rx") == user_repo.get_user_id(
        "0imfnc8mVLWwsAawjYr4Rx"
    )
    assert user_repo.get_user_id("1imfnc8mVLWwsAawjYr4Rx") != user_repo.get_user_id(
        "0imfnc8mVLWwsAawjYr4Rx"
    )
    user_repo.store_user("3imfnc8mVLWwsAawjYr4Rx")
    user_repo.store_user("4imfnc8mVLWwsAawjYr4Rx")
    assert user_repo.get_user_id("3imfnc8mVLWwsAawjYr4Rx") == user_repo.get_user_id(
        "3imfnc8mVLWwsAawjYr4Rx"
    )
    assert user_repo.get_user_id("4imfnc8mVLWwsAawjYr4Rx") != user_repo.get_user_id(
        "0imfnc8mVLWwsAawjYr4Rx"
    )


def test_user_repository_store_get_with_more_input(user_repo: IUserRepository):
    for i in range(1000):
        api_key: str = "apy_key" + str(i)
        user_repo.store_user(api_key)
        assert user_repo.get_user_id(api_key) == i


# def test_wallet_repository_create_wallet(wallet_repo: IUserRepository):
#     pass
#
#
# def test_wallet_repository_get_wallet_amount(wallet_repo: IUserRepository):
#     pass
#
#
# def test_wallet_repository_balance():
#     pass
#
#
# def test_wallet_repository_is_my_wallet():
#     pass
#
#
# def test_wallet_repository_make_transaction():
#     pass
