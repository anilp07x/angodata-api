"""
Serviço de autenticação backed por PostgreSQL (SQLAlchemy).
Expõe a mesma interface do AuthService (JSON) para uso transparente via ServiceFactory.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from flask_bcrypt import Bcrypt
from sqlalchemy.exc import SQLAlchemyError

from src.database.base import get_db_session
from src.database.models import User, UserRole

bcrypt = Bcrypt()


class AuthServiceDB:
    """Serviço de operações de autenticação usando o banco de dados."""

    @staticmethod
    def get_all_users() -> List[Dict[str, Any]]:
        """Retorna todos os usuários (sem senha)."""
        try:
            with get_db_session() as session:
                users = session.query(User).order_by(User.id).all()
                return [u.to_dict() for u in users]
        except SQLAlchemyError as e:
            print(f"Database error getting all users: {e}")
            return []

    @staticmethod
    def get_user_by_id(user_id) -> Optional[Dict[str, Any]]:
        """Retorna um usuário por ID (sem senha)."""
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return None
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                return user.to_dict() if user else None
        except SQLAlchemyError as e:
            print(f"Database error getting user {user_id}: {e}")
            return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Retorna um usuário por email (com password_hash - para autenticação).

        Nota: retorna o hash porque é usado pelo AuthServiceDB.authenticate.
        """
        try:
            with get_db_session() as session:
                user = (
                    session.query(User)
                    .filter(User.email.ilike(email))
                    .first()
                )
                if not user:
                    return None
                data = user.to_dict()
                data["password_hash"] = user.password_hash
                return data
        except SQLAlchemyError as e:
            print(f"Database error getting user by email: {e}")
            return None

    @staticmethod
    def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Retorna um usuário por username (sem senha)."""
        try:
            with get_db_session() as session:
                user = (
                    session.query(User)
                    .filter(User.username.ilike(username))
                    .first()
                )
                return user.to_dict() if user else None
        except SQLAlchemyError as e:
            print(f"Database error getting user by username: {e}")
            return None

    @staticmethod
    def register(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Registra um novo usuário. Retorna None se email/username já existir."""
        try:
            with get_db_session() as session:
                existing = (
                    session.query(User)
                    .filter(
                        (User.email.ilike(data["email"]))
                        | (User.username.ilike(data["username"]))
                    )
                    .first()
                )
                if existing:
                    return None
                user = User(
                    username=data["username"],
                    email=data["email"].lower(),
                    password_hash=bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
                    role=UserRole(data.get("role", "user")),
                    created_at=datetime.utcnow(),
                )
                session.add(user)
                session.flush()
                return user.to_dict()
        except SQLAlchemyError as e:
            print(f"Database error registering user: {e}")
            return None

    @staticmethod
    def verify_password(stored_password_hash: str, provided_password: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return bcrypt.check_password_hash(stored_password_hash, provided_password)

    @staticmethod
    def authenticate(email: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica por email e senha. Retorna dados sem senha se OK."""
        user = AuthServiceDB.get_user_by_email(email)
        if not user:
            return None
        if not AuthServiceDB.verify_password(user["password_hash"], password):
            return None
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"],
        }

    @staticmethod
    def update_user(user_id, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Atualiza dados de um usuário (username, email, password, role)."""
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return None
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    return None
                if "username" in data:
                    user.username = data["username"]
                if "email" in data:
                    user.email = data["email"].lower()
                if "password" in data:
                    user.password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
                if "role" in data:
                    user.role = UserRole(data["role"])
                session.flush()
                return user.to_dict()
        except SQLAlchemyError as e:
            print(f"Database error updating user {user_id}: {e}")
            return None

    @staticmethod
    def delete_user(user_id) -> bool:
        """Deleta um usuário por ID."""
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return False
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
