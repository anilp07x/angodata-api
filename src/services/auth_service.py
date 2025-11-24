"""
Serviço de autenticação e autorização.
Gerencia registro, login e validação de usuários.
"""

from datetime import datetime

from flask_bcrypt import Bcrypt

from src.models.user import USERS
from src.utils.persistence import persist_data

# Instância do Bcrypt para hash de senhas
bcrypt = Bcrypt()


class AuthService:
    """Serviço para operações de autenticação"""

    @staticmethod
    def get_all_users():
        """Retorna todos os usuários (sem senha)"""
        return [
            {"id": u["id"], "username": u["username"], "email": u["email"], "role": u["role"], "created_at": u["created_at"]}
            for u in USERS
        ]

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retorna um usuário por ID (sem senha).

        Args:
            user_id (int): ID do usuário

        Returns:
            dict ou None: Dados do usuário ou None se não encontrado
        """
        user_id = int(user_id)
        for user in USERS:
            if user["id"] == user_id:
                return {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "role": user["role"],
                    "created_at": user["created_at"],
                }
        return None

    @staticmethod
    def get_user_by_email(email):
        """
        Retorna um usuário por email (com senha - para autenticação).

        Args:
            email (str): Email do usuário

        Returns:
            dict ou None: Dados completos do usuário ou None
        """
        for user in USERS:
            if user["email"].lower() == email.lower():
                return user
        return None

    @staticmethod
    def get_user_by_username(username):
        """
        Retorna um usuário por username (sem senha).

        Args:
            username (str): Username do usuário

        Returns:
            dict ou None: Dados do usuário ou None
        """
        for user in USERS:
            if user["username"].lower() == username.lower():
                return {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "role": user["role"],
                    "created_at": user["created_at"],
                }
        return None

    @staticmethod
    @persist_data
    def register(data):
        """
        Registra um novo usuário.

        Args:
            data (dict): Dados do usuário (username, email, password, role)

        Returns:
            dict ou None: Usuário criado (sem senha) ou None se email/username já existe
        """
        # Verificar se email já existe
        if AuthService.get_user_by_email(data["email"]):
            return None  # Email já em uso

        # Verificar se username já existe
        if AuthService.get_user_by_username(data["username"]):
            return None  # Username já em uso

        # Gerar novo ID
        new_id = max([u["id"] for u in USERS]) + 1 if USERS else 1

        # Hash da senha
        password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

        # Criar usuário
        new_user = {
            "id": new_id,
            "username": data["username"],
            "email": data["email"].lower(),
            "password_hash": password_hash,
            "role": data.get("role", "user"),
            "created_at": datetime.utcnow().isoformat(),
        }

        USERS.append(new_user)

        # Retornar sem senha
        return {
            "id": new_user["id"],
            "username": new_user["username"],
            "email": new_user["email"],
            "role": new_user["role"],
            "created_at": new_user["created_at"],
        }

    @staticmethod
    def verify_password(stored_password_hash, provided_password):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.

        Args:
            stored_password_hash (str): Hash da senha armazenada
            provided_password (str): Senha fornecida pelo usuário

        Returns:
            bool: True se senha correta, False caso contrário
        """
        return bcrypt.check_password_hash(stored_password_hash, provided_password)

    @staticmethod
    def authenticate(email, password):
        """
        Autentica um usuário por email e senha.

        Args:
            email (str): Email do usuário
            password (str): Senha do usuário

        Returns:
            dict ou None: Dados do usuário (sem senha) se autenticado, None caso contrário
        """
        user = AuthService.get_user_by_email(email)

        if not user:
            return None

        if not AuthService.verify_password(user["password_hash"], password):
            return None

        # Retornar dados sem senha
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"],
        }

    @staticmethod
    @persist_data
    def update_user(user_id, data):
        """
        Atualiza dados de um usuário.

        Args:
            user_id (int): ID do usuário
            data (dict): Dados para atualizar

        Returns:
            dict ou None: Usuário atualizado ou None
        """
        user_id = int(user_id)
        for user in USERS:
            if user["id"] == user_id:
                if "username" in data:
                    user["username"] = data["username"]
                if "email" in data:
                    user["email"] = data["email"].lower()
                if "password" in data:
                    user["password_hash"] = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
                if "role" in data:
                    user["role"] = data["role"]

                return {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "role": user["role"],
                    "created_at": user["created_at"],
                }
        return None

    @staticmethod
    @persist_data
    def delete_user(user_id):
        """
        Deleta um usuário.

        Args:
            user_id (int): ID do usuário

        Returns:
            bool: True se deletado, False se não encontrado
        """
        user_id = int(user_id)
        for i, user in enumerate(USERS):
            if user["id"] == user_id:
                USERS.pop(i)
                return True
        return False
