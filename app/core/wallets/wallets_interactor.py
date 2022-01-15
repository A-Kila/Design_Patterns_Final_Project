from typing import Protocol


class IRateApi(Protocol):
    def get_rate(self, currency: str) -> float:
        pass


class IWalletRepository:
    pass


class WalletsInteractor:
    wallet_repo: IWalletRepository
