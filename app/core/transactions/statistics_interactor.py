from dataclasses import dataclass

from app.core.interfaces.exception_handle_interface import IExceptionHandler
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
    expection_handler: IExceptionHandler
    ADMIN_API_KEY: str = "admin123"  # Super secure password

    def get_statistics(self, request: StatisticsGetRequest) -> StatisticsGetResponse:
        if request.admin_api_key != self.ADMIN_API_KEY:
            raise self.expection_handler.user_access_denied

        stats: Statistics = self.transaction_repo.get_statistics()
        return StatisticsGetResponse(
            number_of_transactions=stats.total_transactions,
            platform_profit=stats.total_profit,
        )
