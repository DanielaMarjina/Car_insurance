from fastapi import HTTPException

from app.api.routers import insurance_policy
from app.api.schemas.insurance_policy_schemas import InsurancePolicyCreate
from app.db.models import InsurancePolicy
from app.repositories.car_repository.base import CarRepository
from app.repositories.insurance_policy_repository.base import InsurancePolicyRepository


class InsurancePolicyService:
    def __init__(self, repository: InsurancePolicyRepository):
        self.repository = repository

    def create_insurance_policy(self, request: InsurancePolicyCreate):
        car_id = request.car_id

        if car_id:
            existing_car = CarRepository.get_by_car_id(car_id)

            if existing_car:
                insurance_policy = InsurancePolicy(
                    car_id=car_id,
                    provider=request.provider,
                    start_date=request.start_date,
                    end_date=request.end_date,
                    paid_amount=request.paid_amount,
                )
            else:
                raise HTTPException(status_code=400, detail="Car not found")

        return self.repository.create(insurance_policy)
