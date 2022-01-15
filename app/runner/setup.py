from fastapi import FastAPI

from app.core.facade import WalletService
from app.infra.fastapi.api import wallet_api
from app.infra.in_memory.user_in_memory import UserInMemoryRepository


def setup() -> FastAPI:
    app = FastAPI()

    app.include_router(wallet_api)
    app.state.core = WalletService.create(UserInMemoryRepository())

    return app
