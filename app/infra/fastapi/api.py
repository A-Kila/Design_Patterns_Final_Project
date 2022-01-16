from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.core.facade import CreateTransactionRequest, UsersResponse, WalletService
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


@wallet_api.post("/users")
def register_user(core: WalletService = Depends(get_core)) -> UsersResponse:
    return core.register_user()


@wallet_api.post("/wallets")
def create_wallet(
    api_key: str, core: WalletService = Depends(get_core)
) -> WalletResponse:
    return core.create_wallet(WalletPostRequest(api_key))


@wallet_api.get("/wallet/{address}")
def get_wallet(
    api_key: str, address: str, core: WalletService = Depends(get_core)
) -> WalletResponse:
    return core.get_wallet(WalletGetRequest(api_key, address))


@wallet_api.post("/transaction")
def perform_transaction(
    request: CreateTransactionRequest, core: WalletService = Depends(get_core)
) -> None:
    core.make_transaction(request)


@wallet_api.get("/transactions")
def get_transactions(
    api_key: str, core: WalletService = Depends(get_core)
) -> GetTransactionsResponse:
    return core.get_transactions(GetUserTransactionsRequest(api_key))


@wallet_api.get("/wallet/{address}/transactions")
def get_wallet_transactions(
    api_key: str, address: str, core: WalletService = Depends(get_core)
) -> GetTransactionsResponse:
    return core.get_wallet_transactions(WalletTransactionsRequest(api_key, address))


@wallet_api.get("/statistics")
def get_statistics(admin_key: str, core: WalletService = Depends(get_core)) -> str:
    pass
