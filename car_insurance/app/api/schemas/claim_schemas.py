from datetime import date
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.exceptions.amount_exceptions import AmountValidationError
from app.exceptions.description_exceptions import DescriptionValidationError


class ClaimCreate(BaseModel):
    claim_date: date
    description: str
    amount: int

    @field_validator("description")
    @classmethod
    def validate_description(cls, description: str) -> str:
        if len(description) > 2000:
            raise DescriptionValidationError(description)

        return description

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, amount: int) -> int:
        if amount <= 0:
            raise AmountValidationError(amount)

        return amount

class ClaimResponse(BaseModel):
    id:UUID
    car_id:UUID
    claim_date:date
    description:str
    amount:int