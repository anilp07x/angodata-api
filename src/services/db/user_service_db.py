"""
User service using SQLAlchemy ORM.
Provides database-backed operations for users.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.exc import SQLAlchemyError

from src.database.base import get_db_session
from src.database.models import User, UserRole


class UserServiceDB:
    """Service for managing users with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        Get all users from database.

        Returns:
            List[Dict]: List of all users with their data
        """
        try:
            with get_db_session() as session:
                users = session.query(User).order_by(User.username).all()
                return [user.to_dict() for user in users]
        except SQLAlchemyError as e:
            print(f"Database error getting all users: {e}")
            return []

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific user by ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            Dict or None: User data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                return user.to_dict() if user else None
        except SQLAlchemyError as e:
            print(f"Database error getting user {user_id}: {e}")
            return None

    @staticmethod
    def get_by_username(username: str) -> Optional[Dict[str, Any]]:
        """
        Get a user by username.

        Args:
            username: Username to search for

        Returns:
            Dict or None: User data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.username == username).first()
                return user.to_dict() if user else None
        except SQLAlchemyError as e:
            print(f"Database error getting user by username '{username}': {e}")
            return None

    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Get a user by email.

        Args:
            email: Email to search for

        Returns:
            Dict or None: User data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.email == email).first()
                return user.to_dict() if user else None
        except SQLAlchemyError as e:
            print(f"Database error getting user by email '{email}': {e}")
            return None

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new user.

        Args:
            data: User data (username, email, password_hash, role)

        Returns:
            Dict or None: Created user data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                # Convert role string to enum if needed
                role = data.get("role", "user")
                if isinstance(role, str):
                    role = UserRole[role]

                user = User(
                    username=data["username"],
                    email=data["email"],
                    password_hash=data["password_hash"],
                    role=role,
                    created_at=datetime.utcnow(),
                )
                session.add(user)
                session.flush()
                result = user.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error creating user: {e}")
            return None

    @staticmethod
    def update(user_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing user.

        Args:
            user_id: ID of the user to update
            data: Updated user data

        Returns:
            Dict or None: Updated user data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.id == user_id).first()

                if not user:
                    return None

                # Update fields if provided
                if "username" in data:
                    user.username = data["username"]
                if "email" in data:
                    user.email = data["email"]
                if "password_hash" in data:
                    user.password_hash = data["password_hash"]
                if "role" in data:
                    role = data["role"]
                    if isinstance(role, str):
                        role = UserRole[role]
                    user.role = role

                session.flush()
                result = user.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error updating user {user_id}: {e}")
            return None

    @staticmethod
    def delete(user_id: int) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: ID of the user to delete

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.id == user_id).first()

                if not user:
                    return False

                session.delete(user)
                return True
        except SQLAlchemyError as e:
            print(f"Database error deleting user {user_id}: {e}")
            return False

    @staticmethod
    def count() -> int:
        """
        Get total count of users.

        Returns:
            int: Total number of users
        """
        try:
            with get_db_session() as session:
                return session.query(User).count()
        except SQLAlchemyError as e:
            print(f"Database error counting users: {e}")
            return 0
