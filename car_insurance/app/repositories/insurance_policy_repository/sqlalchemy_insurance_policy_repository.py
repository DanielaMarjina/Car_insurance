from _pydatetime import date
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.sql import Select
from sqlalchemy.orm import Session

from app.api.routers import insurance_policy
from app.api.schemas.owner_schemas import OwnerUpdate
from app.db.models import Owner, InsurancePolicy
from app.exceptions.owner_exceptions import OwnerNotFoundError
from app.repositories.insurance_policy_repository.base import InsurancePolicyRepository
from app.repositories.owner_repository.base import OwnerRepository
from app.repositories.paginator import PaginationRepositoryMixin
from app.utils.enums.driver_license_category import DriverLicenseCategory


class SqlAlchemyInsurancePolicyRepository(PaginationRepositoryMixin, InsurancePolicyRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_insurance_policy(
            self,
            page: int,
            per_page: int,
            id: UUID,
            car_id: UUID,
            provider: str,
            start_date: date,
            end_date: date,
            paid_amount: int,
            status: str,
    ):
        statement = self._apply_filters(
            select(InsurancePolicy),
            car_id=car_id,
            provider=provider,
            start_date=start_date,
            end_date=end_date,
            paid_amount=paid_amount,
            status=status,

        )

        return self.paginate_query(statement, page=page, per_page=per_page)

    def create(self, policy: InsurancePolicy) -> InsurancePolicy:
        self.db.add(insurance_policy)
        self.db.commit()
        self.db.refresh(insurance_policy)

        return insurance_policy


    def _apply_filters(
            self,
            statement: Select,
    ) -> Select:
        filters = []

        if not filters:
            return statement

        return statement.where(*filters)

    @staticmethod
    def _escape_like(value: str) -> str:
        return (
            value
            .replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
        )
