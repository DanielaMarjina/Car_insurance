import logging
from typing import Literal
from uuid import UUID

from app.api.schemas.car_history import CarHistoryResponse, CarHistoryPolicyResponse, CarHistoryClaimResponse
from app.exceptions.car_exceptions import CarNotFoundError
from app.repositories.car_repository.base import CarRepository
from app.repositories.claim_repository.base import ClaimRepository
from app.repositories.insurance_policy_repository.base import InsurancePolicyRepository

logger = logging.getLogger(__name__)


class CarHistoryService:

    def __init__(self, insurance_policy_repository: InsurancePolicyRepository, claim_repository: ClaimRepository,
                 car_repository: CarRepository):
        self.insurance_policy_repository = insurance_policy_repository
        self.claim_repository = claim_repository
        self.car_repository = car_repository

    def get_car_history(self, car_id: UUID, type: Literal["POLICY", "CLAIM"] | None = None,) -> list[CarHistoryResponse]:
        logger.info(f"Getting car history for {car_id}")
        existing_car = self.car_repository.get_by_car_id(car_id)

        if not existing_car:
            logger.warning(f"Car with id {car_id} not found")
            raise CarNotFoundError(car_id)

        policies = self.insurance_policy_repository.get_by_car_id(car_id)

        claims = self.claim_repository.get_by_car_id(car_id)

        history = []

        if type != "CLAIM":
            for policy in policies:
                history.append(
                    CarHistoryPolicyResponse(
                        type="POLICY",
                        policy_id=policy.id,
                        start_date=policy.start_date,
                        end_date=policy.end_date,
                        provider=policy.provider,
                        paid_amount=policy.paid_amount,
                        status=policy.status,
                    )
                )

        if type != "POLICY":
            for claim in claims:
                history.append(
                    CarHistoryClaimResponse(
                        type="CLAIM",
                        claim_id=claim.id,
                        claim_date=claim.claim_date,
                        amount=claim.amount,
                        description=claim.description,
                    )
                )



        history.sort(key=lambda x: x.start_date if x.type=="POLICY" else x.claim_date, reverse=True)

        logger.info(f"Found {len(history)} history items")
        return history