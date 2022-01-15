from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.core.facade import UsersResponse, WalletService

wallet_api: APIRouter = APIRouter()


def get_core(request: Request) -> WalletService:
    service: WalletService = request.app.state.core
    return service


@wallet_api.post("/users")
def register_user(core: WalletService = Depends(get_core)) -> UsersResponse:
    return core.register_user()


@wallet_api.post("/wallets")
def create_wallet(api_key: str, core: WalletService = Depends(get_core)) -> str:
    pass


@wallet_api.get("/wallet/{address}")
def get_wallet(api_key: str, core: WalletService = Depends(get_core)) -> str:
    pass


@wallet_api.post("/transaction")
def perform_transaction(api_key: str, core: WalletService = Depends(get_core)) -> None:
    pass


@wallet_api.get("/transactions")
def get_transactions(api_key: str, core: WalletService = Depends(get_core)) -> str:
    pass


@wallet_api.get("/wallet/{address}/transactions")
def get_wallet_transactions(
    api_key: str, core: WalletService = Depends(get_core)
) -> str:
    pass


@wallet_api.get("/statistics")
def get_statistics(admin_key: str, core: WalletService = Depends(get_core)) -> str:
    pass
