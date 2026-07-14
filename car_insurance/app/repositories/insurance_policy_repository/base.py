
from typing import Protocol
from datetime import date
from uuid import UUID

from app.api.schemas.insurance_policy_schemas import InsurancePolicyDetailResponse
from app.db.models import InsurancePolicy
from app.utils.enums.status import Status


class InsurancePolicyRepository(Protocol):

    def get_policies(self,
                     page: int,
                     per_page: int,
                     provider:str | None = None,
                     status: Status | None = None,
                     )->list[InsurancePolicy]:...

    def get_active_policy_for_car(self, car_id : UUID)->InsurancePolicyDetailResponse:...

    def create_insurance_policy(
            self,
            request: InsurancePolicy,
    ) ->InsurancePolicy: ...

    def has_valid_insurance_policy(
            self,
            car_id:UUID,
            date:date
    )->bool:...

    def get_by_car_id(
            self,
            car_id:UUID,
    )->list[InsurancePolicy]:...


