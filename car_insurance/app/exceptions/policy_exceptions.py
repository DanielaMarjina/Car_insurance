from uuid import UUID

from starlette import status

from app.utils.custom_exception import AppException


class PolicyNotFoundError(AppException):
    def __init__(self, car_id: UUID):
        super().__init__(
            message=f"Car with id {car_id} does not have an active policy",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="active_policy_for_car_not_found",
        )