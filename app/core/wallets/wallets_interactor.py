from dataclasses import dataclass

from app.core.interfaces.users_interface import IUserRepository
from app.core.interfaces.wallets_interface import IRateApi, IWalletRepository
from app.core.interfaces.exception_handle_interface import IExceptionHandler


@dataclass
class WalletGetRequest:
    api_key: str
    wallet_address: str


@dataclass
class WalletPostRequest:
    api_key: str


@dataclass
class WalletResponse:
    balance_btc: float
    balance_usd: float
    wallet_address: str


@dataclass
class WalletsInteractor:
    user_repo: IUserRepository
    wallet_repo: IWalletRepository
    rate_getter: IRateApi
    exeption_handler: IExceptionHandler

    INITIAL_WALLET_BALANCE: int = 100000000
    MAX_WALLET_COUNT: int = 3

    def create_wallet(self, request: WalletPostRequest) -> WalletResponse:
        api_key: str = request.api_key
        user_id: int = self.user_repo.get_user_id(api_key=api_key)
        number_of_wallets: int = self.wallet_repo.get_wallet_count(user_id=user_id)

        if number_of_wallets >= self.MAX_WALLET_COUNT:
            raise self.exeption_handler.max_wallets

        wallet_address: str = f"{user_id}_{number_of_wallets + 1}"
        balance = self.INITIAL_WALLET_BALANCE

        self.wallet_repo.create_wallet(
            user_id=user_id,
            wallet_address=wallet_address,
            balance=balance,
        )

        balance_btc = self.sats_to_btc(wallet_balance_sats=balance)
        balance_usd = self.btc_to_usd(wallet_balance_btc=balance_btc)

        return WalletResponse(
            balance_btc=balance_btc,
            balance_usd=balance_usd,
            wallet_address=wallet_address,
        )

    def sats_to_btc(self, wallet_balance_sats: float) -> float:
        sats_to_btc: float = self.rate_getter.get_rate("sats")
        return wallet_balance_sats / sats_to_btc

    def btc_to_usd(self, wallet_balance_btc: float) -> float:
        usd_to_btc: float = self.rate_getter.get_rate("usd")
        return wallet_balance_btc * usd_to_btc

    def get_wallet(self, request: WalletGetRequest) -> WalletResponse:
        address: str = request.wallet_address
        user_id: int = self.user_repo.get_user_id(request.api_key)

        if not self.wallet_repo.wallet_exists(request.wallet_address):
            raise self.exeption_handler.no_wallet

        if not self.wallet_repo.is_my_wallet(user_id, request.wallet_address):
            raise self.exeption_handler.wallet_access_denied

        wallet_balance_sats: float = self.wallet_repo.get_balance(
            request.wallet_address
        )

        wallet_balance_btc: float = self.sats_to_btc(wallet_balance_sats)
        wallet_balance_usd: float = self.btc_to_usd(wallet_balance_btc)

        return WalletResponse(
            wallet_address=address,
            balance_usd=wallet_balance_usd,
            balance_btc=wallet_balance_btc,
        )
