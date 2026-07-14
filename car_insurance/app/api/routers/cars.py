from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_car_service
from app.api.responses import error_responses
from app.api.schemas.car_schemas import CarDetailResponse, CarCreate
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.services.car_service import CarService
from app.utils.enums.car_category import CarCategory

cars_router = APIRouter(prefix="/api/cars", tags=["Cars"])


@cars_router.get(
    "/cars-categories",
    response_model=list[str],
    summary="Get car categories",
    description="Returns the available car categories.",
    responses=error_responses(404),

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


@cars_router.post(
    "/",
    response_model=CarDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create car",
    description=("Create a new car."),
    responses=error_responses(400, 409, 500),
)
def create_car(
        car_data: CarCreate,
        car_service: CarService = Depends(get_car_service),
):
    return car_service.create_car(car_data)


@cars_router.delete(
    "/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete car",
    description=(
            "Delete a car by its ID."
    ),
    responses=error_responses(404, 500),
)
def delete_car(car_id: UUID, car_service: CarService = Depends(get_car_service),)->None:
    car_service.delete_car(car_id)
