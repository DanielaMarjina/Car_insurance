from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging

from app.api.routers.car_history import car_history_router
from app.api.routers.cars import cars_router
from app.api.routers.claim import claim_router
from app.api.routers.health import health_router
from app.api.routers.insurance_policy import insurance_policy_router
from app.api.routers.licenses import licenses_router
from app.api.routers.owners import owners_router
from app.exceptions.register_handlers import register_custom_exception_handlers
from app.middleware.pagination import PaginationMiddleware
from app.utils.logging import configure_logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Insurance API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # Allow all headers
)
configure_logging()
logger.info("Application started")
app.add_middleware(PaginationMiddleware)

app.include_router(licenses_router)
app.include_router(owners_router)
app.include_router(cars_router)
register_custom_exception_handlers(app)

app.include_router(health_router)

app.include_router(insurance_policy_router)

app.include_router(claim_router)

app.include_router(car_history_router)
