import pytest

from app.core.interfaces.transitions_interface import Transaction
from app.core.transactions.tax_calculator import FreeTax
from app.core.transactions.transactions_interactor import (
    CreateTransactionRequest,
    GetTransactionsResponse,
    GetUserTransactionsRequest,
    TransactionInteractor,
    WalletTransactionsRequest,
)
from app.core.users.users_interactor import UsersInteractor, UsersResponse
from app.core.wallets.wallets_interactor import (
    WalletPostRequest,
    WalletResponse,
    WalletsInteractor,
)
from app.infra.in_memory.transactions_repository import TransactionRepositoryInMemory
from app.infra.in_memory.user_in_memory import UserInMemoryRepository
from app.infra.in_memory.wallet_repository import InMemoryWalletRepository
from app.infra.rateapi.coingecko import CoinGeckoApi


@pytest.fixture()
def transaction_interactor() -> TransactionInteractor:
    return TransactionInteractor(
        transaction_repo=TransactionRepositoryInMemory(),
        user_repo=UserInMemoryRepository(),
        wallet_repo=InMemoryWalletRepository(),
    )


def test_success_transaction(transaction_interactor: TransactionInteractor):
    users_interactor: UsersInteractor = UsersInteractor(
        user_repo=transaction_interactor.user_repo
    )
    wallet_interactor: WalletsInteractor = WalletsInteractor(
        user_repo=transaction_interactor.user_repo,
        wallet_repo=transaction_interactor.wallet_repo,
        rate_getter=CoinGeckoApi(),
    )

    user: UsersResponse = users_interactor.generate_new_api_key()
    api_key: str = user.api_key
    user_id: int = users_interactor.user_repo.get_user_id(api_key=api_key)

    request_wallet = WalletPostRequest(api_key=api_key)
    wallet_1: WalletResponse = wallet_interactor.create_wallet(request=request_wallet)
    wallet_2: WalletResponse = wallet_interactor.create_wallet(request=request_wallet)

    request: CreateTransactionRequest = CreateTransactionRequest(
        api_key=api_key,
        wallet_to=wallet_1.wallet_address,
        wallet_from=wallet_2.wallet_address,
        amount=100,
    )

    transaction_interactor.make_transaction(request=request)

    get_request = GetUserTransactionsRequest(api_key=api_key)
    response: GetTransactionsResponse = transaction_interactor.get_transactions(
        request=get_request
    )

    transactions: list[Transaction] = response.transactions
    transaction: Transaction = transactions[0]

    assert transaction.user_id == user_id
    assert transaction.to_wallet == wallet_1.wallet_address
    assert transaction.from_wallet == wallet_2.wallet_address
    assert transaction.amount == 100
    assert transaction.profit == FreeTax().tax_rate


def test_make_transaction_with_invalid_wallet(
    transaction_interactor: TransactionInteractor,
):
    users_interactor: UsersInteractor = UsersInteractor(
        user_repo=transaction_interactor.user_repo
    )
    wallet_interactor: WalletsInteractor = WalletsInteractor(
        user_repo=transaction_interactor.user_repo,
        wallet_repo=transaction_interactor.wallet_repo,
        rate_getter=CoinGeckoApi(),
    )

    user: UsersResponse = users_interactor.generate_new_api_key()

    request_wallet = WalletPostRequest(api_key=user.api_key)
    wallet: WalletResponse = wallet_interactor.create_wallet(request=request_wallet)

    request_1: CreateTransactionRequest = CreateTransactionRequest(
        api_key=user.api_key,
        wallet_to="Invalid_wallet",
        wallet_from=wallet.wallet_address,
        amount=100,
    )

    with pytest.raises(Exception):
        transaction_interactor.make_transaction(request=request_1)

    request_2: CreateTransactionRequest = CreateTransactionRequest(
        api_key=user.api_key,
        wallet_to=wallet.wallet_address,
        wallet_from="Invalid_wallet",
        amount=100,
    )

    with pytest.raises(Exception):
        transaction_interactor.make_transaction(request=request_2)


def test_make_transaction_with_other_user(
    transaction_interactor: TransactionInteractor,
):
    users_interactor: UsersInteractor = UsersInteractor(
        user_repo=transaction_interactor.user_repo
    )
    wallet_interactor: WalletsInteractor = WalletsInteractor(
        user_repo=transaction_interactor.user_repo,
        wallet_repo=transaction_interactor.wallet_repo,
        rate_getter=CoinGeckoApi(),
    )

    user_1: UsersResponse = users_interactor.generate_new_api_key()
    user_2: UsersResponse = users_interactor.generate_new_api_key()

    request_wallet = WalletPostRequest(api_key=user_1.api_key)
    wallet_1: WalletResponse = wallet_interactor.create_wallet(request=request_wallet)
    wallet_2: WalletResponse = wallet_interactor.create_wallet(request=request_wallet)

    request: CreateTransactionRequest = CreateTransactionRequest(
        api_key=user_2.api_key,
        wallet_to=wallet_1.wallet_address,
        wallet_from=wallet_2.wallet_address,
        amount=100,
    )

    with pytest.raises(Exception):
        transaction_interactor.make_transaction(request=request)


def test_get_transactions_with_invalid_wallet(
    transaction_interactor: TransactionInteractor,
):
    users_interactor: UsersInteractor = UsersInteractor(
        user_repo=transaction_interactor.user_repo
    )

    user: UsersResponse = users_interactor.generate_new_api_key()
    api_key: str = user.api_key

    request = WalletTransactionsRequest(
        api_key=api_key, wallet_address="Invalid_wallet"
    )
    with pytest.raises(Exception):
        transaction_interactor.get_wallet_transactions(request=request)
