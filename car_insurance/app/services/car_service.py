from typing import List
from uuid import UUID

from app.api.schemas.car_schemas import CarDetailResponse
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.db.models import Car
from app.repositories.car_repository.base import CarRepository
from app.utils.enums import car_category
from app.utils.enums.car_category import CarCategory


class CarService:
    def __init__(self, repository: CarRepository) -> None:
            self.repository = repository

    def get_by_id(self, car_id: UUID) -> Car:
        car = self.repository.get_car_by_id(car_id)
        return car

    def get_categories(self) -> List[str]:
        return [category.value for category in CarCategory]

    def get_cars(
            self,
            page: int,
            per_page: int,
            make: str | None = None,
            model: str | None = None,
            category: CarCategory | None = None,
            owner_id: UUID | None = None,
    ) ->PaginatedResponse[CarDetailResponse]:
        return self.repository.get_cars(
            page=page,
            per_page=per_page,
            make=make,
            model=model,
            category=category,
            owner_id=owner_id
        )
