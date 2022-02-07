from typing import Protocol


class IWalletRepository(Protocol):
    def create_wallet(self, user_id: int, wallet_address: str, balance: float) -> None:
        pass

    def get_wallet_count(self, user_id: int) -> int:
        pass

    def get_balance(self, wallet_address: str) -> float:
        pass

    def wallet_exists(self, wallet_address: str) -> bool:
        pass

    def is_my_wallet(self, user_id: int, wallet_address: str) -> bool:
        pass

    def make_transaction(
        self, from_wallet: str, to_wallet: str, amount_from: float, amount_to: float
    ) -> None:
        pass

    def take_money(self, from_wallet: str, amount: float) -> None:
        pass

    def give_money(self, to_wallet: str, amount: float) -> None:
        pass


class IRateApi(Protocol):
    def get_rate(self, currency: str) -> float:
        pass
