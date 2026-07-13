from uuid import UUID
import re
from pydantic import BaseModel, ConfigDict, field_validator

from app.api.schemas.owner_schemas import OwnerResponse
from app.exceptions.car_exceptions import CarValidationError
from app.utils.enums.car_category import CarCategory


class CarDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vin:str
    make:str | None
    model:str | None
    year_of_manufacture:int
    category: CarCategory | None
    cc:int
    power:int
    owner:OwnerResponse

_VIN_PATTERN = re.compile(r"^[A-Za-z0-9]{17}$")
_NAME_PATTERN = re.compile(r"^(?=.{1,150}$)[A-Za-z0-9]+(?: [A-Za-z0-9]+)*$")


class CarCreate(BaseModel):
    vin: str
    make: str | None = None
    model: str | None = None
    year_of_manufacture: int
    category: CarCategory | None = None
    cc: int
    power: int
    owner_id:UUID

    @field_validator("vin")
    @classmethod
    def validate_vin(cls, vin: str) -> str:
        if not _VIN_PATTERN.fullmatch(vin):
            raise CarValidationError(
                "VIN must contain exactly 17 alphanumeric characters"
            )

        return vin

    @field_validator("make", "model")
    @classmethod
    def validate_make_model(cls, value: str | None) -> str | None:
        if value is None:
            return None

        if not _NAME_PATTERN.fullmatch(value):
            raise CarValidationError(
                "Value must contain only letters, numbers and single spaces "
                "and must be between 1 and 150 characters"
            )

        return value

    @field_validator("cc")
    @classmethod
    def validate_cc(cls, cc: int) -> int:
        if not (0 <= cc <= 10000):
            raise CarValidationError(
                "Engine capacity must be between 0 and 10000 cc"
            )

        return cc

    @field_validator("power")
    @classmethod
    def validate_power(cls, power: int) -> int:
        if not (0 <= power <= 500):
            raise CarValidationError(
                "Power must be between 0 and 500 HP"
            )

        return power