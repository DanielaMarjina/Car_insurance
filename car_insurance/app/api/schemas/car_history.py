from datetime import date
from typing import Literal, Union
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CarHistoryPolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type:Literal["POLICY"]
    policy_id:UUID
    start_date: date
    end_date: date
    provider:str
    paid_amount:float
    status:str

class CarHistoryClaimResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type : Literal["CLAIM"]
    claim_id:UUID
    claim_date: date
    amount:float
    description:str

CarHistoryResponse = Union[CarHistoryPolicyResponse, CarHistoryClaimResponse]

