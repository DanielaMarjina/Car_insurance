
from typing import Protocol
from datetime import date
from uuid import UUID

from app.db.models import InsurancePolicy


class InsurancePolicyRepository(Protocol):


    def create_insurance_policy(
            self,
            request: InsurancePolicy,
    ) ->InsurancePolicy: ...

    def has_valid_insurance_policy(
            self,
            car_id:UUID,
            date:date
    )->bool:...


