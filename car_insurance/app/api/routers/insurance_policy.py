from fastapi import APIRouter,status

from app.api.schemas.insurance_policy_schemas import InsurancePolicyDetailResponse

insurance_policy_router=APIRouter(prefix="/api/cars", tags=["Insurance Policy"])
@insurance_policy_router.get("/cars")

@insurance_policy_router.post(
    path="/{carId}/policies",
    response_model=InsurancePolicyDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an insurance policy",
    description="Create an insurance policy for an existing car.",
)
def create_insurance_policy()