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


@pytest.fixture()
def setup(self, repo: IUserRepository):
    self.repo = self.repo


# test_in_memory_user_repository
def test_user_repository_store_user(repo: IUserRepository):
    repo.store_user("0imfnc8mVLWwsAawjYr4Rx")
    repo.store_user("1imfnc8mVLWwsAawjYr4Rx")
    repo.store_user("2imfnc8mVLWwsAawjYr4Rx")
    repo.store_user("3imfnc8mVLWwsAawjYr4Rx")


def test_user_repository_get_user(repo: IUserRepository):
    repo.store_user("0imfnc8mVLWwsAawjYr4Rx")
    repo.store_user("1imfnc8mVLWwsAawjYr4Rx")
    repo.store_user("2imfnc8mVLWwsAawjYr4Rx")
    repo.store_user("3imfnc8mVLWwsAawjYr4Rx")
    assert repo.get_user_id("1imfnc8mVLWwsAawjYr4Rx") != repo.get_user_id("0imfnc8mVLWwsAawjYr4Rx")




