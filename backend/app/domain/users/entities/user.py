from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class UserEntity:
    """User entity in the domain layer"""
    id: UUID
    email: str
    hashed_password: str
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        email: str,
        hashed_password: str,
        first_name: str,
        last_name: str,
        is_active: bool = True,
        is_superuser: bool = False,
        id: Optional[UUID] = None,
    ) -> "UserEntity":
        """Factory method to create a new user"""
        now = datetime.utcnow()
        return cls(
            id=id or uuid4(),
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_superuser=is_superuser,
            created_at=now,
            updated_at=now,
        )