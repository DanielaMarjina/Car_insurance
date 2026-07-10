from _pydatetime import date
from uuid import UUID

from typing import Protocol

from app.api.schemas.pagination_schemas import PaginatedResponse
from app.db.models import InsurancePolicy


class InsurancePolicyRepository(Protocol):
    def get_insurance_policy(
            self,
            page: int,
            per_page: int,
            id: UUID,
            car_id: UUID,
            provider: str,
            start_date: date,
            end_date: date,
            paid_amount: int,
            status: str,
    ) -> PaginatedResponse: ...

    def create_insurance_policy(
            self,
            request: InsurancePolicy,
    ) ->InsurancePolicy: ...


