from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.api.responses import error_responses
from app.api.schemas.claim_schemas import ClaimResponse, ClaimCreate
from app.services.claim_service import ClaimService
from app.api.deps import get_claim_service

claim_router = APIRouter(prefix="/api/cars", tags=["Claim"])

@claim_router.post(
    path="/{car_id}/claims",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new claim",
    description="Create a new claim for an existing car",
    responses=error_responses(404, 422),
)
def create_claim(car_id:UUID, request:ClaimCreate, claim_service: ClaimService=Depends(get_claim_service),):
    return claim_service.create_claim(car_id, request)