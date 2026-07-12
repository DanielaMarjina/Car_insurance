from fastapi import HTTPException
from uuid import UUID

from app.api.schemas.claim_schemas import ClaimCreate
from app.db.models import Claim
from app.repositories.car_repository.base import CarRepository
from app.repositories.claim_repository.base import ClaimRepository


class ClaimService:
    def __init__(self, claim_repository: ClaimRepository, car_repository: CarRepository):
        self.claim_repository = claim_repository
        self.car_repository = car_repository

    def create_claim(self, car_id: UUID, request: ClaimCreate) -> Claim:
        existing_car = self.car_repository.get_by_car_id(car_id)

        if not existing_car:
            raise HTTPException(status_code=404, detail="Car not found")

        if request.amount<=0:
            raise HTTPException(status_code=400, detail="Amount cannot be negative or zero")

        if request.amount>=1000000:
            raise HTTPException(status_code=400, detail="Amount cannot be greater than 1000000")


        if not request.description.strip():
            raise HTTPException(status_code=400, detail="Must enter a description")

        claim = Claim(
            car_id=car_id,
            claim_date=request.claim_date,
            description=request.description,
            amount=request.amount,
        )

        return self.claim_repository.create_claim(claim)

