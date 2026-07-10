from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.api.schemas.owner_schemas import OwnerResponse
from app.db.models import Car
from app.utils.enums.car_category import CarCategory

class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vin: str
    make: str | None
    model: str | None



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