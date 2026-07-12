from datetime import date

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

        if request.amount>1000000:
            raise HTTPException(status_code=400, detail="Amount cannot be 1000000 or greater")

        if len(request.description)>2000:
            raise HTTPException(status_code=400, detail="Description must be less than 2000 characters")

        if not request.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")

        if request.claim_date<date(1900,1,1):
            raise HTTPException(status_code=400, detail="Claim date cannot be before 1900-01-01")

        if request.claim_date>date.today():
            raise HTTPException(status_code=400, detail="Claim date cannot be after today's date")

        claim = Claim(
            car_id=car_id,
            claim_date=request.claim_date,
            description=request.description,
            amount=request.amount,
        )

        return self.claim_repository.create_claim(claim)

