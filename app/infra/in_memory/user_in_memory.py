from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserInMemoryRepository:
    repo: dict[str, int] = field(default_factory=dict[str, int])
    user_count: int = 0

    def store_user(self, api_key: str) -> None:
        self.repo[api_key] = self.user_count
        self.user_count += 1

    def get_user_id(self, api_key: str) -> Optional[int]:
        return self.repo[api_key] if api_key in self.repo else None
