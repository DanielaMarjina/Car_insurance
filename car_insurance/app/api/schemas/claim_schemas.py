from datetime import date
from uuid import UUID

from pydantic import BaseModel


class ClaimCreate(BaseModel):
    claim_date: date
    description: str
    amount: int


class ClaimResponse(BaseModel):
    id:UUID
    car_id:UUID
    claim_date:date
    description:str
    amount:int