import pytest

from app.core.interfaces.users_interface import IUserRepository
from app.infra.in_memory.user_in_memory import UserInMemoryRepository


@pytest.fixture()
def starting_user_id() -> int:
    return 0


@pytest.fixture()
def user_repo() -> IUserRepository:
    return UserInMemoryRepository()


def test_user_repository_store_get_user(user_repo: IUserRepository) -> None:
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


def test_user_repository_store_get_with_more_input(
    starting_user_id: int, user_repo: IUserRepository
) -> None:
    for i in range(1000):
        api_key: str = "apy_key" + str(i)
        user_repo.store_user(api_key)
        cur_id: int = user_repo.get_user_id(api_key)
        assert cur_id == starting_user_id + i
