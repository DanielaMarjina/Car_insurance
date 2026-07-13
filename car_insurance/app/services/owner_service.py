from uuid import UUID
import logging
from app.api.schemas.owner_schemas import OwnerCreate, OwnerDetailResponse, OwnerUpdate
from app.api.schemas.pagination_schemas import PaginatedResponse
from app.db.models import Owner
from app.exceptions.owner_exceptions import OwnerEmailAlreadyExistsError
from app.repositories.owner_repository.base import OwnerRepository
from app.utils.enums.driver_license_category import DriverLicenseCategory

logger = logging.getLogger(__name__)

class OwnerService:
    def __init__(self, repository: OwnerRepository):
        self.repository = repository

    def get_owners(
        self,
        page: int = 1,
        per_page: int = 50,
        category: list[DriverLicenseCategory] | None = None,
        email: str | None = None,
    ) -> PaginatedResponse[OwnerDetailResponse]:
        logger.info("Retrieving owners")
        return self.repository.get_owners(
            page=page,
            per_page=per_page,
            category=category,
            email=email,
        )

    def create_owner(self, request: OwnerCreate) -> Owner:
        logger.info("Creating owner '%s'", request.name)

        email = request.email

        if email:
            existing_owner = self.repository.get_by_email(email)

            if existing_owner:
                logger.warning("Owner with email %s already exists", email)
                raise OwnerEmailAlreadyExistsError(email)

        owner = Owner(
            name=request.name,
            birthdate=request.birthdate,
            year_of_driver_license=request.year_of_driver_license,
            driver_license_cat=request.driver_license_cat,
            email=email,
        )
        created_owner = self.repository.create(owner)

        logger.info("Owner %s created successfully", created_owner.id)

        return created_owner

    def get_owner_by_id(self, owner_id: UUID) -> Owner:
        owner = self.repository.get_by_id(owner_id)
        logger.info("Retrieving owner %s", owner_id)

        return owner

    def patch_owner(self, owner_id: UUID, request: OwnerUpdate) -> Owner:
        owner = self.repository.get_by_id(owner_id)
        logger.info("Updating owner %s", owner_id)

        if request.email is not None:
            email = request.email
            existing_owner = self.repository.get_by_email(email)

            if existing_owner and existing_owner.id != owner_id:
                logger.warning(
                    "Cannot update owner %s. Email %s already exists.",
                    owner_id,
                    email,
                )
                raise OwnerEmailAlreadyExistsError(email)

            request = request.model_copy(update={"email": email})

        updated_owner = self.repository.update(owner, request)
        logger.info("Owner %s updated successfully", owner_id)

        return updated_owner

    def delete_owner(self, owner_id: UUID) -> None:
        logger.info("Deleting owner %s", owner_id)
        owner = self.repository.get_by_id(owner_id)

        self.repository.delete_owner(owner)
        logger.info("Deleted owner %s", owner_id)
