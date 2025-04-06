from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.users.entities.user import UserEntity
from app.domain.users.interfaces.user_repository import UserRepository
from app.infrastructure.database.models.user import User


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        """Get a user by ID"""
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        db_user = result.scalars().first()
        if not db_user:
            return None
        return self._map_to_entity(db_user)

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Get a user by email"""
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        db_user = result.scalars().first()
        if not db_user:
            return None
        return self._map_to_entity(db_user)

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        """Get a list of users"""
        query = select(User).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return [self._map_to_entity(user) for user in result.scalars().all()]

    async def create(self, user: UserEntity) -> UserEntity:
        """Create a new user"""
        db_user = User(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return self._map_to_entity(db_user)

    async def update(self, user: UserEntity) -> UserEntity:
        """Update an existing user"""
        db_user = await self.session.get(User, user.id)
        if db_user:
            db_user.email = user.email
            db_user.hashed_password = user.hashed_password
            db_user.first_name = user.first_name
            db_user.last_name = user.last_name
            db_user.is_active = user.is_active
            db_user.is_superuser = user.is_superuser
            db_user.updated_at = user.updated_at
            await self.session.commit()
            await self.session.refresh(db_user)
        return self._map_to_entity(db_user)

    async def delete(self, user_id: UUID) -> bool:
        """Delete a user"""
        db_user = await self.session.get(User, user_id)
        if db_user:
            await self.session.delete(db_user)
            await self.session.commit()
            return True
        return False

    def _map_to_entity(self, db_user: User) -> UserEntity:
        """Map DB model to domain entity"""
        return UserEntity(
            id=db_user.id,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            is_active=db_user.is_active,
            is_superuser=db_user.is_superuser,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )