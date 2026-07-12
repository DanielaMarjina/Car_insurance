from uuid import UUID

from fastapi import APIRouter, Depends, Query,status

from app.api.deps import get_car_service
from app.api.schemas.car_schemas import CarDetailResponse
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.services.car_service import CarService
from app.utils.enums.car_category import CarCategory

cars_router = APIRouter(prefix="/api/cars", tags=["Cars"])


@cars_router.get(
    "/cars-categories",
    response_model=list[str],
    summary="Get car categories",
    description="Returns the available car categories.",
)
def get_car_categories(car_service: CarService = Depends(get_car_service),
                       ) -> list[str]:
    return car_service.get_categories()


@cars_router.get(
    path="/",
    response_model=PaginatedResponse[CarDetailResponse],
    summary="Get cars",
    description="Returns all cars.",
)
def get_cars(
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=50, ge=1, le=100),
        make: str | None = None,
        model: str | None = None,
        category: CarCategory | None = None,
        owner_id: UUID | None = None,
        car_service: CarService = Depends(get_car_service),
) -> PaginatedResponse[CarDetailResponse]:
    return car_service.get_cars(
        page=page,
        per_page=per_page,
        make=make,
        model=model,
        category=category,
        owner_id=owner_id
    )

