from dataclasses import dataclass

from app.core.interfaces.exception_handle_interface import IExceptionHandler
from app.core.interfaces.users_interface import IUserRepository
from app.core.interfaces.wallets_interface import IRateApi, IWalletRepository
from app.core.wallets.address_generator import SimpleAddressGenerator
from app.core.wallets.currency_converter import BitcoinConverter
from definitions import MAX_WALLET_COUNT, INITIAL_WALLET_BALANCE


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
    exception_handler: IExceptionHandler

    def create_wallet(self, request: WalletPostRequest) -> WalletResponse:
        api_key: str = request.api_key
        user_id: int = self.user_repo.get_user_id(api_key=api_key)
        number_of_wallets: int = self.wallet_repo.get_wallet_count(user_id=user_id)

        if number_of_wallets >= MAX_WALLET_COUNT:
            raise self.exception_handler.max_wallets

        wallet_address: str = SimpleAddressGenerator.generate_address(user_id, number_of_wallets)
        balance = INITIAL_WALLET_BALANCE

        self.wallet_repo.create_wallet(
            user_id=user_id,
            wallet_address=wallet_address,
            balance=balance,
        )

        balance_btc = BitcoinConverter.convert_from(balance, "sats", self.rate_getter)
        balance_usd = BitcoinConverter.convert_to(balance_btc, "usd", self.rate_getter)

        return WalletResponse(
            balance_btc=balance_btc,
            balance_usd=balance_usd,
            wallet_address=wallet_address,
        )

    def get_wallet(self, request: WalletGetRequest) -> WalletResponse:
        address: str = request.wallet_address
        user_id: int = self.user_repo.get_user_id(request.api_key)

        if not self.wallet_repo.wallet_exists(request.wallet_address):
            raise self.exception_handler.no_wallet

        if not self.wallet_repo.is_my_wallet(user_id, request.wallet_address):
            raise self.exception_handler.wallet_access_denied

        wallet_balance_sats: float = self.wallet_repo.get_balance(
            request.wallet_address
        )

        wallet_balance_btc: float = BitcoinConverter.convert_from(wallet_balance_sats, "sats", self.rate_getter)
        wallet_balance_usd: float = BitcoinConverter.convert_to(wallet_balance_btc, "usd", self.rate_getter)

        return WalletResponse(
            wallet_address=address,
            balance_usd=wallet_balance_usd,
            balance_btc=wallet_balance_btc,
        )
