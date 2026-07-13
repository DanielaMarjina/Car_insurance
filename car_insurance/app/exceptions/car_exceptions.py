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

class CarValidationError(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="car_validation_error",
        )

class CarAlreadyExistsError(AppException):
    def __init__(self, vin: str):
        super().__init__(
            message=f"Car with vin {vin} already exists",
            status_code=status.HTTP_409_CONFLICT,
            error_code="car_vin_already_exists",
        )
