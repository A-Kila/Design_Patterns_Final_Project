from dataclasses import dataclass

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
    ADMIN_API_KEY: str = "admin123"

    def get_statistics(self, request: StatisticsGetRequest) -> StatisticsGetResponse:
        if request.admin_api_key != self.ADMIN_API_KEY:
            raise Exception("you are not the admin")
        stats: Statistics = self.transaction_repo.get_statistics()
        return StatisticsGetResponse(
            number_of_transactions=stats.total_transactions,
            platform_profit=stats.total_profit,
        )
