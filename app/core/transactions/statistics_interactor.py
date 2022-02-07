from dataclasses import dataclass

from fastapi import HTTPException, status

from app.core.interfaces.transitions_interface import ITransactionRepository, Statistics


@dataclass
class StatisticsGetRequest:
    admin_api_key: str


@dataclass
class StatisticsGetResponse:
    number_of_transactions: int
    platform_profit: float


@dataclass
class StatisticsInteractor:
    transaction_repo: ITransactionRepository
    ADMIN_API_KEY: str = "admin123"     # Super secure password

    def get_statistics(self, request: StatisticsGetRequest) -> StatisticsGetResponse:
        if request.admin_api_key != self.ADMIN_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied"
            )

        stats: Statistics = self.transaction_repo.get_statistics()
        return StatisticsGetResponse(
            number_of_transactions=stats.total_transactions,
            platform_profit=stats.total_profit,
        )
