from starlette import status

from app.utils.custom_exception import AppException

class ProviderValidationError(AppException):
    def __init__(self, provider:str):
        super().__init__(
            message=f"Provider {provider} must contain at least 1 character and at most 100 character",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="provider_validation_error",
        )

class ProviderFormatValidationError(AppException):
    def __init__(self, provider:str):
        super().__init__(
            message=f"Provider {provider} must contain only letters and numbers and separated only by one space",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="provider_format_validation_error",
        )
