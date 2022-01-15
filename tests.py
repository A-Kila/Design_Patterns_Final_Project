# def store_user(self, api_key: str) -> None:
#     self.repo[api_key] = self.user_count
#     self.user_count += 1
# def get_user_id(self, api_key: str) -> Optional[int]:
#     return self.repo[api_key] if api_key in self.repo else None
import pytest

from app.core.users.users_interactor import IUserRepository
from app.infra.in_memory.user_in_memory import UserInMemoryRepository


@pytest.fixture()
def repo() -> IUserRepository:
    return UserInMemoryRepository()


def test_user_repository_store_get_user(repo: IUserRepository):
    repo.store_user("0imfnc8mVLWwsAawjYr4Rx")
    repo.store_user("1imfnc8mVLWwsAawjYr4Rx")
    assert repo.get_user_id("0imfnc8mVLWwsAawjYr4Rx") == repo.get_user_id("0imfnc8mVLWwsAawjYr4Rx")
    assert repo.get_user_id("1imfnc8mVLWwsAawjYr4Rx") != repo.get_user_id("0imfnc8mVLWwsAawjYr4Rx")
    repo.store_user("3imfnc8mVLWwsAawjYr4Rx")
    repo.store_user("4imfnc8mVLWwsAawjYr4Rx")
    assert repo.get_user_id("3imfnc8mVLWwsAawjYr4Rx") == repo.get_user_id("3imfnc8mVLWwsAawjYr4Rx")
    assert repo.get_user_id("4imfnc8mVLWwsAawjYr4Rx") != repo.get_user_id("0imfnc8mVLWwsAawjYr4Rx")


def test_user_repository_store_get_with_more_input(repo: IUserRepository):
    for i in range(1000):
        repo.store_user("apy_key" + i)
        assert repo.get_user_id("apy_key" + i) is int




