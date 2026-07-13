from starlette import status

from app.utils.custom_exception import AppException

class DescriptionValidationError(AppException):
    def __init__(self, description:str):
        super().__init__(
            message=f"Description cannot be empty and must be less than 2000 characters",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="description_validation_error",
        )
