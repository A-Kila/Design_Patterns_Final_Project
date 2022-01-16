from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.core.facade import (
    TransactionRequest,
    UsersResponse,
    WalletService,
)
from app.core.transactions.statistics_interactor import StatisticsGetResponse, StatisticsGetRequest
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
    request: TransactionRequest, core: WalletService = Depends(get_core)
) -> None:
    core.make_transaction(request)


@wallet_api.get("/transactions")
def get_transactions(api_key: str, core: WalletService = Depends(get_core)) -> str:
    pass


@wallet_api.get("/wallet/{address}/transactions")
def get_wallet_transactions(
    api_key: str, core: WalletService = Depends(get_core)
) -> str:
    pass


@wallet_api.get("/statistics")
def get_statistics(admin_key: str, core: WalletService = Depends(get_core)) -> StatisticsGetResponse:
    return core.get_statistics(StatisticsGetRequest(admin_key))
