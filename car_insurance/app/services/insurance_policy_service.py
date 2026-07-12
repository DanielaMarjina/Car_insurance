from uuid import UUID

from fastapi import HTTPException
from datetime import date
from app.api.schemas.insurance_policy_schemas import InsurancePolicyCreate, InsuranceValidityResponse
from app.db.models import InsurancePolicy
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
            raise HTTPException(status_code=404, detail="Car not found")

        if request.end_date < request.start_date:
            raise HTTPException(
                status_code=400,
                detail="endDate must be greater than or equal to startDate",
            )

        if request.start_date.year < 1900 and request.end_date.year > 2100:
            raise HTTPException(
                status_code=400,
                detail="The date should be a realistic year, between 1900 and 2100"
            )

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
            raise HTTPException(status_code=404, detail="Car not found")

        if (date.year > 2100
                or date.year < 1900):
            raise HTTPException(
                status_code=400,
                detail="The date should be a realistic year, between 1900 and 2100",
            )

        valid=self.insurance_policy_repository.has_valid_insurance_policy(
            car_id,
            date,
        )

        return InsuranceValidityResponse(car_id=car_id,date=date,valid=valid)
