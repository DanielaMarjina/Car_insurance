from uuid import UUID
import re
from fastapi import HTTPException
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


class InsurancePolicyService:
    def __init__(self, insurance_policy_repository: InsurancePolicyRepository, car_repository: CarRepository):
        self.insurance_policy_repository = insurance_policy_repository
        self.car_repository = car_repository

    def create_insurance_policy(self, car_id: UUID, request: InsurancePolicyCreate):

        existing_car = self.car_repository.get_by_car_id(car_id)

        if not existing_car:
            raise CarNotFoundError(car_id)

        if request.end_date < request.start_date:
            raise EndDateStartDateValidationError(request.start_date, request.end_date)

        if (
                request.start_date.year < 1900
                or request.start_date.year > 2100
                or request.end_date.year < 1900
                or request.end_date.year > 2100
        ):
            raise DateYearValidationError()

        if request.paid_amount <= 0:
            raise AmountValidationError(request.paid_amount)

        if request.paid_amount > 1000000:
            raise AmountValidationError(request.paid_amount)

        if request.provider is not None:

            if len(request.provider) < 1:
                raise ProviderValidationError(request.provider)

            if len(request.provider) > 100:
                raise ProviderValidationError(request.provider)

            if not re.fullmatch(
                    r"[A-Za-z0-9]+( [A-Za-z0-9]+)*",
                    request.provider,
            ):
                raise ProviderFormatValidationError(request.provider)

        insurance_policy = InsurancePolicy(
            car_id=car_id,
            provider=request.provider,
            start_date=request.start_date,
            end_date=request.end_date,
            paid_amount=request.paid_amount,
            status=Status.ACTIVE
        )

        return self.insurance_policy_repository.create_insurance_policy(insurance_policy)

    def has_valid_insurance_policy(self, car_id: UUID, date: date) -> InsuranceValidityResponse:
        existing_car = self.car_repository.get_by_car_id(car_id)

        if not existing_car:
            raise CarNotFoundError(car_id)

        if (date.year > 2100
                or date.year < 1900):
            raise DateYearValidationError()

        valid=self.insurance_policy_repository.has_valid_insurance_policy(
            car_id,
            date,
        )

        return InsuranceValidityResponse(car_id=car_id,date=date,valid=valid)
