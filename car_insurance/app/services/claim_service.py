from datetime import date
import logging
from uuid import UUID

from app.api.schemas.claim_schemas import ClaimCreate
from app.db.models import Claim
from app.exceptions.amount_exceptions import AmountValidationError
from app.exceptions.car_exceptions import CarNotFoundError
from app.exceptions.date_exceptions import ClaimDateValidationError
from app.exceptions.description_exceptions import DescriptionValidationError
from app.repositories.car_repository.base import CarRepository
from app.repositories.claim_repository.base import ClaimRepository

logger = logging.getLogger(__name__)

class ClaimService:
    def __init__(self, claim_repository: ClaimRepository, car_repository: CarRepository):
        self.claim_repository = claim_repository
        self.car_repository = car_repository

    def create_claim(self, car_id: UUID, request: ClaimCreate) -> Claim:
        logger.info(f"Creating claim for {car_id}")
        existing_car = self.car_repository.get_by_car_id(car_id)

        if not existing_car:
            logger.warning("Car with id %s does not exist", car_id)
            raise CarNotFoundError(car_id)

        if request.amount <= 0:
            logger.warning("Amount must be greater than 0")
            raise AmountValidationError(amount=request.amount)

        if request.amount > 1000000:
            logger.warning("Amount must be less than 1000000")
            raise AmountValidationError(amount=request.amount)

        if len(request.description) > 2000:
            logger.warning("Description must be less than 2000")
            raise DescriptionValidationError(description=request.description)

        if not request.description.strip():
            logger.warning("Description cannot be empty")
            raise DescriptionValidationError(description=request.description)

        if request.claim_date < date(1900, 1, 1):
            logger.warning("Claim date must be before 1900-01-01")
            raise ClaimDateValidationError()

        if request.claim_date > date.today():
            logger.warning("Claim date must be before today")
            raise ClaimDateValidationError()

        claim = Claim(
            car_id=car_id,
            claim_date=request.claim_date,
            description=request.description,
            amount=request.amount,
        )

        logger.info(f"Created claim for {car_id}")

        return self.claim_repository.create_claim(claim)
