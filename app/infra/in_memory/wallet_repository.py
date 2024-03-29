from dataclasses import dataclass, field


@dataclass
class InMemoryWalletRepository:
    wallets: dict[str, float] = field(default_factory=dict[str, float])
    number_of_wallets: dict[int, int] = field(default_factory=dict[int, int])
    wallets_for_user: dict[int, list[str]] = field(default_factory=dict[int, list[str]])

    def create_wallet(self, user_id: int, wallet_address: str, balance: float) -> None:
        self.wallets[wallet_address] = balance

        if user_id not in self.wallets_for_user:
            self.wallets_for_user[user_id] = []
        self.wallets_for_user[user_id].append(wallet_address)

        if user_id in self.number_of_wallets:
            self.number_of_wallets[user_id] += 1
        else:
            self.number_of_wallets[user_id] = 1

    def get_wallet_count(self, user_id: int) -> int:
        return self.number_of_wallets.get(user_id, 0)

    def get_balance(self, wallet_address: str) -> float:
        return self.wallets.get(wallet_address, -1)

    def wallet_exists(self, wallet_address: str) -> bool:
        return wallet_address in self.wallets

    def is_my_wallet(self, user_id: int, wallet_address: str) -> bool:
        wallet_list: list[str] = self.wallets_for_user.get(user_id, [])

        return wallet_address in wallet_list

    def make_transaction(
        self, from_wallet: str, to_wallet: str, amount_from: float, amount_to: float
    ) -> None:
        self.take_money(from_wallet, amount_from)
        self.give_money(to_wallet, amount_to)

    def take_money(self, from_wallet: str, amount: float) -> None:
        self.wallets[from_wallet] -= amount

    def give_money(self, to_wallet: str, amount: float) -> None:
        self.wallets[to_wallet] += amount
