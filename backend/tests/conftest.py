import asyncio
import pytest
from typing import AsyncGenerator, Generator, List
from uuid import UUID, uuid4

from app.domain.users.entities.user import UserEntity
from app.domain.users.interfaces.user_repository import UserRepository
from app.domain.users.services.user_service import UserService


class MockUserRepository(UserRepository):
    """Mock implementation of UserRepository for testing"""
    
    def __init__(self):
        self.users: List[UserEntity] = []
    
    async def get_by_id(self, user_id: UUID) -> UserEntity:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    async def get_by_email(self, email: str) -> UserEntity:
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        return self.users[skip:skip+limit]
    
    async def create(self, user: UserEntity) -> UserEntity:
        self.users.append(user)
        return user
    
    async def update(self, user: UserEntity) -> UserEntity:
        for i, existing_user in enumerate(self.users):
            if existing_user.id == user.id:
                self.users[i] = user
                return user
        return None
    
    async def delete(self, user_id: UUID) -> bool:
        for i, user in enumerate(self.users):
            if user.id == user_id:
                self.users.pop(i)
                return True
        return False


@pytest.fixture
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def user_repository() -> AsyncGenerator[UserRepository, None]:
    """Fixture for user repository"""
    repo = MockUserRepository()
    
    # Add some test users
    user1 = UserEntity.create(
        email="user1@example.com",
        hashed_password="password1",
        first_name="User",
        last_name="One",
    )
    user2 = UserEntity.create(
        email="user2@example.com",
        hashed_password="password2",
        first_name="User",
        last_name="Two",
    )
    
    await repo.create(user1)
    await repo.create(user2)
    
    yield repo


@pytest.fixture
async def user_service(user_repository: UserRepository) -> UserService:
    """Fixture for user service"""
    return UserService(user_repository)