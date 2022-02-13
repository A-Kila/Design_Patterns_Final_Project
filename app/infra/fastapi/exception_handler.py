from fastapi import HTTPException, status


class HttpExceptionHandler:
    @property
    def invalid_api_key(self) -> Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied"
        )

    @property
    def user_access_denied(self) -> Exception:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
        )

    @property
    def no_wallet(self) -> Exception:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Wallet address"
        )

    @property
    def wallet_access_denied(self) -> Exception:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This Wallet doesn't Belong to You",
        )

    @property
    def max_wallets(self) -> Exception:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has maximum amount of wallets",
        )

    @property
    def not_enough_money(self) -> Exception:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough money on wallet",
        )
