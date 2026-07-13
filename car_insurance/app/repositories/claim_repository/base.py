from typing import Protocol
from uuid import UUID

from app.db.models import Claim


class ClaimRepository(Protocol):
    def create_claim(
            self,
            claim: Claim,
    ) -> Claim: ...

    def get_by_car_id(
            self,
            car_id:UUID,
    )->list[Claim]:...