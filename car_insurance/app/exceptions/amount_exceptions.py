from starlette import status

from app.utils.custom_exception import AppException


class AmountValidationError(AppException):
    def __init__(self, amount:int):
        super().__init__(
            message=f"Paid amount {amount} must be greater than 0, less than or equal to 1000000",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="amount_validation_error",
        )
