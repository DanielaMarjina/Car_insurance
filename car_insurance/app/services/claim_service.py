from datetime import date

from fastapi import HTTPException
from uuid import UUID

from app.api.schemas.claim_schemas import ClaimCreate
from app.db.models import Claim
from app.exceptions.amount_exceptions import AmountValidationError
from app.exceptions.car_exceptions import CarNotFoundError
from app.exceptions.date_exceptions import ClaimDateValidationError
from app.exceptions.description_exceptions import DescriptionValidationError
from app.repositories.car_repository.base import CarRepository
from app.repositories.claim_repository.base import ClaimRepository


class ClaimService:
    def __init__(self, claim_repository: ClaimRepository, car_repository: CarRepository):
        self.claim_repository = claim_repository
        self.car_repository = car_repository

    def create_claim(self, car_id: UUID, request: ClaimCreate) -> Claim:
        existing_car = self.car_repository.get_by_car_id(car_id)

        if not existing_car:
            raise CarNotFoundError(car_id)

        if request.amount <= 0:
            raise AmountValidationError(amount=request.amount)

        if request.amount > 1000000:
            raise AmountValidationError(amount=request.amount)
        if len(request.description) > 2000:
            raise DescriptionValidationError(description=request.description)

        if not request.description.strip():
            raise DescriptionValidationError(description=request.description)

        if request.claim_date < date(1900, 1, 1):
            raise ClaimDateValidationError()

        if request.claim_date > date.today():
            raise ClaimDateValidationError()

        claim = Claim(
            car_id=car_id,
            claim_date=request.claim_date,
            description=request.description,
            amount=request.amount,
        )

        return self.claim_repository.create_claim(claim)
