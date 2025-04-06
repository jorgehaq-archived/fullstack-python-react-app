from datetime import datetime
from typing import List, Optional

import strawberry
from uuid import UUID

from app.domain.users.entities.user import UserEntity


@strawberry.type
class User:
    id: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "User":
        """Convert domain entity to GraphQL type"""
        return cls(
            id=str(entity.id),
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


@strawberry.input
class UserCreateInput:
    email: str
    password: str
    first_name: str
    last_name: str
    is_active: bool = True
    is_superuser: bool = False


@strawberry.input
class UserUpdateInput:
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None