from typing import Generator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.users.interfaces.user_repository import UserRepository
from app.domain.users.services.user_service import UserService
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.user.user_repository_impl import SQLAlchemyUserRepository


async def get_db() -> Generator:
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Dependency for user repository"""
    return SQLAlchemyUserRepository(db)


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """Dependency for user service"""
    return UserService(user_repository)