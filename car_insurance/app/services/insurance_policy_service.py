from uuid import UUID
import re
import logging
from datetime import date
from app.api.schemas.insurance_policy_schemas import InsurancePolicyCreate, InsuranceValidityResponse
from app.db.models import InsurancePolicy
from app.exceptions.amount_exceptions import AmountValidationError
from app.exceptions.car_exceptions import CarNotFoundError
from app.exceptions.date_exceptions import EndDateStartDateValidationError, DateYearValidationError
from app.exceptions.provider_exceptions import ProviderValidationError, ProviderFormatValidationError
from app.repositories.car_repository.base import CarRepository
from app.repositories.insurance_policy_repository.base import InsurancePolicyRepository
from app.utils.enums.status import Status

logger = logging.getLogger(__name__)

class InsurancePolicyService:
    def __init__(self, insurance_policy_repository: InsurancePolicyRepository, car_repository: CarRepository):
        self.insurance_policy_repository = insurance_policy_repository
        self.car_repository = car_repository

    def create_insurance_policy(self, car_id: UUID, request: InsurancePolicyCreate):
        logger.info(f"Creating insurance policy for {car_id}")
        existing_car = self.car_repository.get_by_car_id(car_id)

        if not existing_car:
            logger.warning(f"Car with id {car_id} does not exist")
            raise CarNotFoundError(car_id)

        if request.end_date < request.start_date:
            logger.warning(f"End date {request.end_date} is before start date {request.start_date}")
            raise EndDateStartDateValidationError(request.start_date, request.end_date)

        if (
                request.start_date.year < 1900
                or request.start_date.year > 2100
                or request.end_date.year < 1900
                or request.end_date.year > 2100
        ):
            logger.warning("One of the years is before 1900 or after 2100")
            raise DateYearValidationError()

        if request.paid_amount <= 0:
            logger.warning(f"Paid amount {request.paid_amount} is less than 0")
            raise AmountValidationError(request.paid_amount)

        if request.paid_amount > 1000000:
            logger.warning(f"Paid amount {request.paid_amount} is greater than 1000000")
            raise AmountValidationError(request.paid_amount)

        if request.provider is not None:

            if len(request.provider) < 1:
                logger.warning(f"Provider {request.provider} is empty")
                raise ProviderValidationError(request.provider)

            if len(request.provider) > 100:
                logger.warning(f"Provider {request.provider} is longer than 100 characters")
                raise ProviderValidationError(request.provider)

            if not re.fullmatch(
                    r"[A-Za-z0-9]+( [A-Za-z0-9]+)*",
                    request.provider,
            ):
                logger.warning(f"Provider {request.provider} is invalid")
                raise ProviderFormatValidationError(request.provider)

        insurance_policy = InsurancePolicy(
            car_id=car_id,
            provider=request.provider,
            start_date=request.start_date,
            end_date=request.end_date,
            paid_amount=request.paid_amount,
            status=Status.ACTIVE
        )
        logger.info(f"Created insurance policy for {car_id}")

        return self.insurance_policy_repository.create_insurance_policy(insurance_policy)

    def has_valid_insurance_policy(self, car_id: UUID, date: date) -> InsuranceValidityResponse:
        logger.info(f"Validating insurance policy for {car_id}")

        existing_car = self.car_repository.get_by_car_id(car_id)

        if not existing_car:
            logger.warning(f"Car with id {car_id} does not exist")
            raise CarNotFoundError(car_id)

        if (date.year > 2100
                or date.year < 1900):
            logger.warning(f"Year {date.year} is before 1900 or after 2100")
            raise DateYearValidationError()

        valid=self.insurance_policy_repository.has_valid_insurance_policy(
            car_id,
            date,
        )
        logger.info(f"Valid insurance policy for {car_id}")
        return InsuranceValidityResponse(car_id=car_id,date=date,valid=valid)
