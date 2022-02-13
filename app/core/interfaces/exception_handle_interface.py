from typing import Protocol


class IExceptionHandler(Protocol):
    @property
    def invalid_api_key(self) -> Exception:
        pass

    @property
    def user_access_denied(self) -> Exception:
        pass

    @property
    def no_wallet(self) -> Exception:
        pass

    @property
    def wallet_access_denied(self) -> Exception:
        pass

    @property
    def max_wallets(self) -> Exception:
        pass

    @property
    def not_enough_money(self) -> Exception:
        pass
