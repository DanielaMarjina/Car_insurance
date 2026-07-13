from datetime import date

from starlette import status

from app.utils.custom_exception import AppException


class EndDateStartDateValidationError(AppException):
    def __init__(self, start_date: date, end_date: date):
        super().__init__(
            message=f"EndDate {end_date} is earlier than StartDate {start_date}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="endDate_startDate_validation_error",
        )

class DateYearValidationError(AppException):
    def __init__(self):
        super().__init__(
            message=f"Year cannot be earlier than 1900 and later than 2100",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="date_year_validation_error",
        )

class ClaimDateValidationError(AppException):
    def __init__(self):
        super().__init__(
            message=f"Claim date cannot be before 1900-01-01 or after today's date",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="claim_date_validation_error",
        )
