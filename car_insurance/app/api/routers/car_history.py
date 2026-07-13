from uuid import UUID

from fastapi import APIRouter, Depends
from app.api.deps import get_car_history_service
from app.api.schemas.car_history import CarHistoryResponse
from app.services.car_history_sevice import CarHistoryService

car_history_router = APIRouter(prefix="/api/cars", tags=["Car History"])


@car_history_router.get("/{car_id}/history", response_model=list[CarHistoryResponse])
def get_car_history(car_id: UUID, car_history_service: CarHistoryService = Depends(get_car_history_service), ):
    return car_history_service.get_car_history(car_id)
