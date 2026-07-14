from fastapi import APIRouter, Query, Depends

from app.api.deps import get_insurance_policy_service
from app.api.schemas.insurance_policy_schemas import InsurancePolicyDetailResponse
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.services.insurance_policy_service import InsurancePolicyService
from app.utils.enums.status import Status

policies_router = APIRouter(prefix="/api/policies", tags=["Insurance Policy"])


@policies_router.get(
    path="/",
    response_model=PaginatedResponse[InsurancePolicyDetailResponse],
    summary="Get policies",
    description="Returns all policies",
)
def get_policies(
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=50, ge=1, le=100),
        provider:str = Query(default="Groupama", description="Provider name"),
        status:Status = Query(default="ACTIVE", description="Status of the policy"),
        insurance_policy_service: InsurancePolicyService = Depends(get_insurance_policy_service),
) -> PaginatedResponse[InsurancePolicyDetailResponse]:
    return insurance_policy_service.get_policies(
        page=page,
        per_page=per_page,
        provider=provider,
        status=status,
    )