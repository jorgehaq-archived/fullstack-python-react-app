from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.users.entities.user import UserEntity


class UserRepository(ABC):
    """Interface for user repository operations"""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        """Get a user by ID"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get a user by email"""
        pass

    @abstractmethod
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        """Get a list of users"""
        pass

    @abstractmethod
    async def create(self, user: UserEntity) -> UserEntity:
        """Create a new user"""
        pass

    @abstractmethod
    async def update(self, user: UserEntity) -> UserEntity:
        """Update an existing user"""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete a user"""
        pass