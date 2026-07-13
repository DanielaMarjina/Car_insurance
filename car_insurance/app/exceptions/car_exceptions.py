from uuid import UUID

from starlette import status

from app.utils.custom_exception import AppException


class CarNotFoundError(AppException):
    def __init__(self, car_id: UUID):
        super().__init__(
            message=f"Car with id {car_id} was not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="car_not_found",
        )

