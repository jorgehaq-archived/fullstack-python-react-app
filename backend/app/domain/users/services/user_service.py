from typing import List, Optional
from uuid import UUID

from app.core.exceptions import NotFoundException, ValidationException
from app.domain.users.entities.user import UserEntity
from app.domain.users.interfaces.user_repository import UserRepository


class UserService:
    """Service for user operations"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: UUID) -> UserEntity:
        """Get a user by ID"""
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundException(f"User with ID {user_id} not found")
        return user

    async def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        """Get a user by email"""
        return await self.user_repository.get_by_email(email)

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        """Get a list of users"""
        return await self.user_repository.list_users(skip, limit)

    async def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        is_active: bool = True,
        is_superuser: bool = False,
    ) -> UserEntity:
        """Create a new user"""
        # Check if email already exists
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise ValidationException("User with this email already exists")

        # In a real application, we would hash the password here
        hashed_password = password  # Placeholder for actual hashing

        # Create a new user entity
        user = UserEntity.create(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_superuser=is_superuser,
        )

        # Save to repository
        return await self.user_repository.create(user)

    async def update_user(self, user: UserEntity) -> UserEntity:
        """Update an existing user"""
        # Check if user exists
        existing_user = await self.user_repository.get_by_id(user.id)
        if not existing_user:
            raise NotFoundException(f"User with ID {user.id} not found")

        # Update the user
        return await self.user_repository.update(user)

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user"""
        # Check if user exists
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise NotFoundException(f"User with ID {user_id} not found")

        # Delete the user
        return await self.user_repository.delete(user_id)