from dataclasses import dataclass


@dataclass
class InMemoryWalletRepository:

    wallets: dict[str:float]
    number_of_wallets: dict[int:int]

    def create_wallet(self, user_id: int, wallet_address: str, balance: float) -> None:
        self.wallets[wallet_address] = balance

        if user_id in self.number_of_wallets:
            self.number_of_wallets[user_id] = 1
        else:
            self.number_of_wallets[user_id] += 1

    def get_wallet_amount(self, user_id: int):
        return self.number_of_wallets[user_id]

    def get_balance(self, wallet_address: str):
        return self.wallets[wallet_address]
