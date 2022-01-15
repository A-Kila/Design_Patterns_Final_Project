from dataclasses import dataclass, field


@dataclass
class InMemoryWalletRepository:

    wallets: dict[str, float] = field(default_factory=dict[str, float])
    number_of_wallets: dict[int, int] = field(default_factory=dict[int, int])
    wallets_for_user: dict[int, list[str]] = field(default_factory=dict[int, list[str]])

    def create_wallet(self, user_id: int, wallet_address: str, balance: float) -> None:
        self.wallets[wallet_address] = balance
        self.wallets_for_user.get(user_id, []).append(wallet_address)

        if user_id in self.number_of_wallets:
            self.number_of_wallets[user_id] = 1
        else:
            self.number_of_wallets[user_id] += 1

    def get_wallet_amount(self, user_id: int) -> int:
        return self.number_of_wallets.get(user_id, -1)

    def get_balance(self, wallet_address: str) -> float:
        return self.wallets.get(wallet_address, -1)

    def is_my_wallet(self, user_id: int, wallet_address: str) -> bool:
        wallet_list: list[str] = self.wallets_for_user.get(user_id, [])

        for address in wallet_list:
            if address == wallet_address:
                return True

        return False

    def make_transaction(self, from_wallet: str, to_wallet: str, amount: float):
        self.take_money(from_wallet, amount)
        self.give_money(to_wallet, amount)

    def take_money(self, from_wallet: str, amount: float):
        self.wallets[from_wallet] -= amount

    def give_money(self, to_wallet: str, amount: float):
        self.wallets[to_wallet] += amount
