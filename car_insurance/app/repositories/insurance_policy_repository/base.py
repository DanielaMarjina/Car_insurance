
from typing import Protocol

from app.db.models import InsurancePolicy


class InsurancePolicyRepository(Protocol):


    def create_insurance_policy(
            self,
            request: InsurancePolicy,
    ) ->InsurancePolicy: ...


