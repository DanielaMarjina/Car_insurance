from uuid import UUID

from sqlalchemy import select, Select
from sqlalchemy.orm import Session

from app.api.schemas.insurance_policy_schemas import InsurancePolicyDetailResponse
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.db.models import InsurancePolicy
from app.repositories.insurance_policy_repository.base import InsurancePolicyRepository
from app.repositories.paginator import PaginationRepositoryMixin
from app.utils.enums.status import Status


class SqlAlchemyInsurancePolicyRepository(PaginationRepositoryMixin, InsurancePolicyRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_policies(self,
                     page: int,
                     per_page: int,
                     provider:str | None = None,
                     status: Status | None = None,
                     ) -> PaginatedResponse:
        statement = self._apply_filters(
            select(InsurancePolicy),
            provider=provider,
            status=status,
        )

        return self.paginate_query(
            statement,
            page=page,
            per_page=per_page,
        )

    def get_active_policy_for_car(self, car_id : UUID) ->InsurancePolicyDetailResponse:
        statement = select(InsurancePolicy).where(
            InsurancePolicy.car_id == car_id,
            InsurancePolicy.status == Status.ACTIVE,
        )
        return self.db.scalar(statement)

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

    def _apply_filters(
            self,
            statement: Select,
            provider: str | None = None,
            status: Status | None = None,
    ) -> Select:
        filters = []

        if provider:
            filters.append(
                InsurancePolicy.provider.ilike(
                    f"%{self._escape_like(provider)}%",
                    escape="\\",
                )
            )

        if status:
            filters.append(
                InsurancePolicy.status.ilike(
                    f"%{self._escape_like(status)}%",
                    escape="\\",
                )
            )

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

