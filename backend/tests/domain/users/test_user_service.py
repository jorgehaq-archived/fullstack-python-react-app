import pytest
from uuid import uuid4

from app.core.exceptions import NotFoundException, ValidationException
from app.domain.users.services.user_service import UserService


@pytest.mark.asyncio
async def test_get_user(user_service: UserService, user_repository):
    """Test getting a user by ID"""
    # Get first test user
    users = await user_repository.list_users()
    user_id = users[0].id
    
    # Test service
    user = await user_service.get_user(user_id)
    assert user.id == user_id
    assert user.email == "user1@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(user_service: UserService):
    """Test getting a non-existent user"""
    # Try to get non-existent user
    with pytest.raises(NotFoundException):
        await user_service.get_user(uuid4())


@pytest.mark.asyncio
async def test_create_user(user_service: UserService):
    """Test creating a user"""
    # Create new user
    user = await user_service.create_user(
        email="newuser@example.com",
        password="newpassword",
        first_name="New",
        last_name="User",
    )
    
    # Verify user was created
    assert user.email == "newuser@example.com"
    assert user.first_name == "New"
    assert user.last_name == "User"
    
    # Verify we can retrieve the user
    retrieved_user = await user_service.get_user_by_email("newuser@example.com")
    assert retrieved_user is not None
    assert retrieved_user.id == user.id


@pytest.mark.asyncio
async def test_create_user_duplicate_email(user_service: UserService):
    """Test creating a user with duplicate email"""
    # Try to create user with existing email
    with pytest.raises(ValidationException):
        await user_service.create_user(
            email="user1@example.com",  # This email already exists
            password="password",
            first_name="Duplicate",
            last_name="User",
        )


@pytest.mark.asyncio
async def test_list_users(user_service: UserService):
    """Test listing users"""
    users = await user_service.list_users()
    
    # Should have at least 2 users from setup
    assert len(users) >= 2
    
    # Verify user properties
    emails = [user.email for user in users]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails


@pytest.mark.asyncio
async def test_update_user(user_service: UserService, user_repository):
    """Test updating a user"""
    # Get first test user
    users = await user_repository.list_users()
    user = users[0]
    
    # Update user
    user.first_name = "Updated"
    user.last_name = "Name"
    
    updated_user = await user_service.update_user(user)
    
    # Verify update
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"
    
    # Verify we can retrieve the updated user
    retrieved_user = await user_service.get_user(user.id)
    assert retrieved_user.first_name == "Updated"
    assert retrieved_user.last_name == "Name"


@pytest.mark.asyncio
async def test_delete_user(user_service: UserService, user_repository):
    """Test deleting a user"""
    # Get first test user
    users = await user_repository.list_users()
    user_id = users[0].id
    
    # Delete user
    result = await user_service.delete_user(user_id)
    assert result is True
    
    # Verify user was deleted
    with pytest.raises(NotFoundException):
        await user_service.get_user(user_id)