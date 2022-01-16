import pytest

from app.core.users.users_interactor import UsersInteractor
from app.infra.in_memory.user_in_memory import UserInMemoryRepository


@pytest.fixture()
def users_interactor() -> UsersInteractor:
    return UsersInteractor(user_repo=UserInMemoryRepository())


def test_users_interactor_generate_new_api_key(users_interactor: UsersInteractor):
    first_user = users_interactor.generate_new_api_key()
    second_user = users_interactor.generate_new_api_key()
    assert first_user != second_user


def test_users_interactor_generate_new_api_key_multiple_calls(
    users_interactor: UsersInteractor,
):
    for i in range(1000):
        first_user = users_interactor.generate_new_api_key()
        second_user = users_interactor.generate_new_api_key()
        assert first_user != second_user
