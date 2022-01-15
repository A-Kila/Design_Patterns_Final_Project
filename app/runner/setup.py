from fastapi import FastAPI

from app.core.facade import WalletService
from app.infra.fastapi.api import wallet_api


def setup() -> FastAPI:
    app = FastAPI()

    app.include_router(wallet_api)
    app.state.core = WalletService()

    return app
