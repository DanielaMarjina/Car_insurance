from uuid import UUID

from sqlalchemy import select
from sqlalchemy.sql import Select
from sqlalchemy.orm import Session

from app.db.models import Car
from app.repositories.car_repository.base import CarRepository
from app.repositories.paginator import PaginationRepositoryMixin
from app.utils.enums.car_category import CarCategory


class SqlAlchemyCarRepository(PaginationRepositoryMixin, CarRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_cars(
            self,
            page: int,
            per_page: int,
            make: str | None = None,
            model: str | None = None,
            category: CarCategory | None = None,
            owner_id: UUID | None = None,
    ):
        statement = self._apply_filters(
            select(Car),
            make=make,
            model=model,
            category=category,
            owner_id=owner_id,
        )

        return self.paginate_query(
            statement,
            page=page,
            per_page=per_page,
        )

    def create_car(self, car: Car) -> Car:
        self.db.add(car)
        self.db.commit()
        self.db.refresh(car)

        return car

    def get_by_car_id(self, car_id: UUID) -> Car | None:
        statement = select(Car).where(Car.id == car_id)
        return self.db.scalar(statement)

    def get_by_vin(self, vin: str) -> Car | None:
        statement = select(Car).where(Car.vin == vin)
        return self.db.scalar(statement)

    def delete_car(self, car: Car) -> None:

        self.db.delete(car)
        self.db.commit()

    def _apply_filters(
            self,
            statement: Select,
            make: str | None = None,
            model: str | None = None,
            category: CarCategory | None = None,
            owner_id: UUID | None = None,
    ) -> Select:
        filters = []

        if make:
            filters.append(
                Car.make.ilike(
                    f"%{self._escape_like(make)}%",
                    escape="\\",
                )
            )

        if model:
            filters.append(
                Car.model.ilike(
                    f"%{self._escape_like(model)}%",
                    escape="\\",
                )
            )

        if category:
            filters.append(Car.category == category)

        if owner_id:
            filters.append(Car.owner_id == owner_id)

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
