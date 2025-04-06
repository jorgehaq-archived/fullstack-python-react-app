"""
Script to create the initial database migration.
Run this script after defining models and before starting the application.
"""

import asyncio
import os
import sys

# Add the parent directory to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alembic import command
from alembic.config import Config
from app.infrastructure.database.session import Base, engine


async def create_tables():
    """Create database tables if they don't exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully")


def create_migration():
    """Create alembic migration"""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, autogenerate=True, message="Initial migration")
    print("Alembic migration created successfully")


async def main():
    """Main function to create tables and migration"""
    # Create tables
    await create_tables()
    
    # Create alembic migration
    create_migration()


if __name__ == "__main__":
    asyncio.run(main())