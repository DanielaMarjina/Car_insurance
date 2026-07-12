from datetime import date
from uuid import UUID

from pydantic import ConfigDict, BaseModel


class InsurancePolicyCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider:str
    start_date:date
    end_date:date
    paid_amount:int

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