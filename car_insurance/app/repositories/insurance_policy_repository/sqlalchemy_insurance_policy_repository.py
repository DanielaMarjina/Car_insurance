from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import InsurancePolicy
from app.repositories.insurance_policy_repository.base import InsurancePolicyRepository
from app.repositories.paginator import PaginationRepositoryMixin


class SqlAlchemyInsurancePolicyRepository(PaginationRepositoryMixin, InsurancePolicyRepository):
    def __init__(self, db: Session):
        self.db = db


    def create_insurance_policy(self, insurance_policy: InsurancePolicy) -> InsurancePolicy:
        self.db.add(insurance_policy)
        self.db.commit()
        self.db.refresh(insurance_policy)

        return insurance_policy

    def has_valid_insurance_policy(self, car_id, date ):
        statement = select(InsurancePolicy).where(
            InsurancePolicy.car_id == car_id,
            InsurancePolicy.start_date<=date,
            InsurancePolicy.end_date>=date,
        )
        policy= self.db.scalar(statement)

        return policy is not None

    def get_by_car_id(self, car_id:UUID) -> list[InsurancePolicy]:
        statement = select(InsurancePolicy).where(InsurancePolicy.car_id == car_id)
        return list(self.db.scalars(statement).all())
