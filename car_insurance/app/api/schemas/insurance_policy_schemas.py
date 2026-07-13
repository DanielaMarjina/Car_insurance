from datetime import date
from uuid import UUID
import re
from pydantic import ConfigDict, BaseModel, field_validator, model_validator

from app.exceptions.amount_exceptions import AmountValidationError
from app.exceptions.date_exceptions import DateYearValidationError, EndDateStartDateValidationError
from app.exceptions.provider_exceptions import ProviderValidationError
from app.utils.date_validator import DateValidator

_PROVIDER_PATTERN = re.compile(r"^(?=.{1,150}$)[A-Za-z0-9]+(?: [A-Za-z0-9]+)*$")

class InsurancePolicyCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider: str
    start_date: date
    end_date: date
    paid_amount: int

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, provider: str) -> str:
        if not _PROVIDER_PATTERN.fullmatch(provider):
            raise ProviderValidationError()

        return provider

    @field_validator("paid_amount")
    @classmethod
    def validate_paid_amount(cls, paid_amount: int) -> int:
        if paid_amount <= 0 or paid_amount > 1_000_000:
            raise AmountValidationError(paid_amount)

        return paid_amount

    @model_validator(mode="after")
    def validate_dates(self) -> "InsurancePolicyCreate":
        DateValidator.ensure_date_year_at_least(
            self.start_date,
            DateValidator.MIN_YEAR,
            DateYearValidationError(),
        )

        DateValidator.ensure_date_year_at_least(
            self.end_date,
            DateValidator.MIN_YEAR,
            DateYearValidationError()
        )

        if self.end_date < self.start_date:
            raise EndDateStartDateValidationError(self.end_date,self.start_date)

        return self

class InsurancePolicyDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    car_id: UUID
    provider: str
    start_date: date
    end_date: date
    paid_amount: float
    status: str

class InsuranceValidityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    car_id:UUID
    date:date
    valid:bool