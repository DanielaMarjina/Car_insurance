from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Claim
from app.repositories.claim_repository.base import ClaimRepository
from app.repositories.paginator import PaginationRepositoryMixin


class SQLAlchemyClaimRepository(PaginationRepositoryMixin,ClaimRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_claim(
            self,
            claim: Claim,
    ) -> Claim:
        self.db.add(claim)
        self.db.commit()
        self.db.refresh(claim)
        return claim

    def get_by_car_id(self, car_id:UUID) -> list[Claim]:
        statement = select(Claim).where(Claim.car_id == car_id)
        return list(self.db.scalars(statement).all())
