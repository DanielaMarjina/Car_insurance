from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.api.deps import get_insurance_policy_service
from app.api.schemas.insurance_policy_schemas import InsurancePolicyDetailResponse, InsurancePolicyCreate
from app.services.insurance_policy_service import InsurancePolicyService

insurance_policy_router=APIRouter(prefix="/api/cars", tags=["Insurance Policy"])
@insurance_policy_router.post(
    path="/{car_id}/policies",
    response_model=InsurancePolicyDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an insurance policy",
    description="Create an insurance policy for an existing car.",
)
def create_insurance_policy(
        car_id: UUID,
        request:InsurancePolicyCreate,
        insurance_policy_service:InsurancePolicyService =Depends(get_insurance_policy_service),
):
    return insurance_policy_service.create_insurance_policy(car_id,request)