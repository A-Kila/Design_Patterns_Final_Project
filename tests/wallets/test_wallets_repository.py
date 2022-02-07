import pytest

from app.core.interfaces.users_interface import IUserRepository
from app.core.interfaces.wallets_interface import IWalletRepository
from app.infra.in_memory.user_in_memory import UserInMemoryRepository
from app.infra.in_memory.wallet_repository import InMemoryWalletRepository


@pytest.fixture()
def starting_user_id() -> int:
    return 0


@pytest.fixture()
def wallet_repo() -> IWalletRepository:
    return InMemoryWalletRepository()


@pytest.fixture()
def user_repo() -> IUserRepository:
    return UserInMemoryRepository()


def test_wallet_repository_create_wallet(
    starting_user_id: int, user_repo: IUserRepository, wallet_repo: IWalletRepository
) -> None:
    user_repo.store_user("user_0")
    user_id: int = starting_user_id
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    assert wallet_repo.get_wallet_count(user_id) == 1  # needs to be finished


def test_wallet_repository_get_wallet_amount(
    starting_user_id: int, user_repo: IUserRepository, wallet_repo: IWalletRepository
) -> None:
    user_repo.store_user("user_0")
    user_id: int = starting_user_id
    assert wallet_repo.get_wallet_count(user_id) == 0

    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    assert wallet_repo.get_wallet_count(user_id) == 1

    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    assert wallet_repo.get_wallet_count(user_id) == 2

    wallet_repo.create_wallet(user_id, "0wallet3", 1.0)
    assert wallet_repo.get_wallet_count(user_id) == 3


def test_wallet_repository_balance(
    starting_user_id: int, user_repo: IUserRepository, wallet_repo: IWalletRepository
) -> None:
    user_repo.store_user("user_0")
    user_id: int = starting_user_id
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id, "0wallet2", 0.0)
    assert wallet_repo.get_balance("0wallet1") == 1
    wallet_repo.make_transaction("0wallet1", "0wallet2", 1.0, 1.0)
    assert wallet_repo.get_balance("0wallet1") == 0


def test_wallet_repository_wallet_exists(
    wallet_repo: IWalletRepository,
    user_repo: IUserRepository,
    starting_user_id: int,
) -> None:
    user_repo.store_user("user_0")
    user_id: int = starting_user_id
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    assert wallet_repo.wallet_exists("0wallet1") is True
    assert wallet_repo.wallet_exists("wrongwalletaddress") is not True
    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    assert wallet_repo.wallet_exists("0wallet2") is True
    assert wallet_repo.wallet_exists("wrongwalletaddress") is not True


def test_wallet_repository_is_my_wallet(
    wallet_repo: IWalletRepository,
    user_repo: IUserRepository,
    starting_user_id: int,
) -> None:
    user_id: int = starting_user_id
    user_repo.store_user("user_0")
    user_repo.store_user("user_1")
    assert user_repo.get_user_id("user_0") == user_id
    assert user_repo.get_user_id("user_1") == user_id + 1

    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id + 1, "1wallet1", 1.0)

    assert wallet_repo.is_my_wallet(user_id, "0wallet1")  # needs to be finished
    assert not (wallet_repo.is_my_wallet(user_id, "1wallet1"))  # wallet repo failed


def test_wallet_repository_make_transaction(
    wallet_repo: IWalletRepository,
    user_repo: IUserRepository,
    starting_user_id: int,
) -> None:
    user_id: int = starting_user_id
    user_repo.store_user("user_0")
    user_repo.store_user("user_1")
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    wallet_repo.create_wallet(user_id + 1, "1wallet1", 1.0)
    wallet_repo.make_transaction("0wallet1", "1wallet1", 1.0, 1.0)
    assert wallet_repo.get_balance("0wallet1") == 0
    assert wallet_repo.get_balance("1wallet1") == 2
    wallet_repo.make_transaction("1wallet1", "0wallet1", 2.0, 2.0)
    assert wallet_repo.get_balance("1wallet1") == 0
    assert wallet_repo.get_balance("0wallet1") == 2
    wallet_repo.make_transaction("0wallet1", "0wallet2", 2.0, 1.0)
    assert wallet_repo.get_balance("0wallet1") == 0
    assert wallet_repo.get_balance("0wallet2") == 2


def test_wallet_repository_take_money(
    wallet_repo: IWalletRepository,
    user_repo: IUserRepository,
    starting_user_id: int,
) -> None:
    user_id: int = starting_user_id
    user_repo.store_user("user_0")
    user_repo.store_user("user_1")
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    wallet_repo.create_wallet(user_id + 1, "1wallet1", 1.0)
    wallet_repo.take_money("0wallet1", 1.0)
    assert wallet_repo.get_balance("0wallet1") == 0
    wallet_repo.take_money("1wallet1", 0.5)
    assert wallet_repo.get_balance("1wallet1") == 0.5
    wallet_repo.take_money("0wallet2", 0)
    assert wallet_repo.get_balance("0wallet2") == 1


def test_wallet_repository_give_money(
    wallet_repo: IWalletRepository,
    user_repo: IUserRepository,
    starting_user_id: int,
) -> None:
    user_id: int = starting_user_id
    user_repo.store_user("user_0")
    user_repo.store_user("user_1")
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    wallet_repo.create_wallet(user_id + 1, "1wallet1", 1.0)
    wallet_repo.give_money("0wallet1", 1.0)
    assert wallet_repo.get_balance("0wallet1") == 2
    wallet_repo.give_money("1wallet1", 0.5)
    assert wallet_repo.get_balance("1wallet1") == 1.5
    wallet_repo.give_money("0wallet2", 0)
    assert wallet_repo.get_balance("0wallet2") == 1
