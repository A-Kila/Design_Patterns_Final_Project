from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.core.facade import CreateTransactionRequest, UsersResponse, WalletService
from app.core.transactions.statistics_interactor import (
    StatisticsGetRequest,
    StatisticsGetResponse,
)
from app.core.transactions.transactions_interactor import (
    GetTransactionsResponse,
    GetUserTransactionsRequest,
    WalletTransactionsRequest,
)
from app.core.wallets.wallets_interactor import (
    WalletGetRequest,
    WalletPostRequest,
    WalletResponse,
)

wallet_api: APIRouter = APIRouter()


def get_core(request: Request) -> WalletService:
    service: WalletService = request.app.state.core
    return service


def check_api_key(request: Request, api_key: str) -> None:
    core: WalletService = get_core(request)

    if not core.is_user_registered(api_key):
        request.app.state.exception_handler.invalid_api_key()


@wallet_api.post("/users")
def register_user(core: WalletService = Depends(get_core)) -> UsersResponse:
    return core.register_user()


@wallet_api.post("/wallets")
def create_wallet(
    api_key: str,
    core: WalletService = Depends(get_core),
    _: None = Depends(check_api_key),
) -> WalletResponse:
    return core.create_wallet(WalletPostRequest(api_key))


@wallet_api.get("/wallet/{address}")
def get_wallet(
    api_key: str,
    address: str,
    core: WalletService = Depends(get_core),
    _: None = Depends(check_api_key),
) -> WalletResponse:
    return core.get_wallet(WalletGetRequest(api_key, address))


@wallet_api.post("/transaction")
def perform_transaction(
    api_key: str,
    wallet_from: str,
    wallet_to: str,
    amount: float,
    core: WalletService = Depends(get_core),
    _: None = Depends(check_api_key),
) -> None:
    core.make_transaction(
        CreateTransactionRequest(api_key, wallet_from, wallet_to, amount)
    )


@wallet_api.get("/transactions")
def get_transactions(
    api_key: str,
    core: WalletService = Depends(get_core),
    _: None = Depends(check_api_key),
) -> GetTransactionsResponse:
    return core.get_transactions(GetUserTransactionsRequest(api_key))


@wallet_api.get("/wallet/{address}/transactions")
def get_wallet_transactions(
    api_key: str,
    address: str,
    core: WalletService = Depends(get_core),
    _: None = Depends(check_api_key),
) -> GetTransactionsResponse:
    return core.get_wallet_transactions(WalletTransactionsRequest(api_key, address))


@wallet_api.get("/statistics")
def get_statistics(
    admin_key: str, core: WalletService = Depends(get_core)
) -> StatisticsGetResponse:
    return core.get_statistics(StatisticsGetRequest(admin_key))
