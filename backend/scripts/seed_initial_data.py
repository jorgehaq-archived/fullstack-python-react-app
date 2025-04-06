"""
Script to seed initial data into the database.
Run this script after migrations are applied.
"""

import asyncio
import os
import sys
from uuid import uuid4

# Add the parent directory to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.domain.users.entities.user import UserEntity
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepository


async def seed_admin_user():
    """Seed an admin user"""
    async with SessionLocal() as session:
        repository = SQLAlchemyUserRepository(session)
        
        # Check if admin already exists
        existing_admin = await repository.get_by_email("admin@example.com")
        if existing_admin:
            print("Admin user already exists, skipping")
            return
        
        # Create admin user
        admin = UserEntity.create(
            email="admin@example.com",
            hashed_password="adminpassword",  # This should be properly hashed in production
            first_name="Admin",
            last_name="User",
            is_active=True,
            is_superuser=True,
        )
        
        await repository.create(admin)
        print("Admin user created successfully")


async def main():
    """Main function to seed initial data"""
    await seed_admin_user()
    print("Initial data seeded successfully")


if __name__ == "__main__":
    asyncio.run(main())