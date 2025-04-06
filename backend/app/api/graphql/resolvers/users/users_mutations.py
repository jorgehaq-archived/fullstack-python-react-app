from typing import List, Optional
from uuid import UUID

import strawberry
from strawberry.types import Info

from app.api.deps import get_user_service
from app.api.graphql.types.user import User, UserCreateInput, UserUpdateInput
from app.domain.users.services.user_service import UserService


@strawberry.type
class UserQuery:
    @strawberry.field
    async def user(self, info: Info, id: str) -> Optional[User]:
        """Get a user by ID"""
        user_service = await get_user_service(info.context["request"])
        user = await user_service.get_user(UUID(id))
        return User.from_entity(user) if user else None

    @strawberry.field
    async def users(self, info: Info, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users"""
        user_service = await get_user_service(info.context["request"])
        users = await user_service.list_users(skip, limit)
        return [User.from_entity(user) for user in users]


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def create_user(self, info: Info, input: UserCreateInput) -> User:
        """Create a new user"""
        user_service = await get_user_service(info.context["request"])
        user = await user_service.create_user(
            email=input.email,
            password=input.password,
            first_name=input.first_name,
            last_name=input.last_name,
            is_active=input.is_active,
            is_superuser=input.is_superuser,
        )
        return User.from_entity(user)

    @strawberry.mutation
    async def update_user(self, info: Info, id: str, input: UserUpdateInput) -> User:
        """Update an existing user"""
        user_service = await get_user_service(info.context["request"])
        
        # Get existing user
        existing_user = await user_service.get_user(UUID(id))
        
        # Apply updates
        if input.email is not None:
            existing_user.email = input.email
        if input.first_name is not None:
            existing_user.first_name = input.first_name
        if input.last_name is not None:
            existing_user.last_name = input.last_name
        if input.is_active is not None:
            existing_user.is_active = input.is_active
        if input.is_superuser is not None:
            existing_user.is_superuser = input.is_superuser
        
        # Update user
        updated_user = await user_service.update_user(existing_user)
        return User.from_entity(updated_user)

    @strawberry.mutation
    async def delete_user(self, info: Info, id: str) -> bool:
        """Delete a user"""
        user_service = await get_user_service(info.context["request"])
        return await user_service.delete_user(UUID(id))