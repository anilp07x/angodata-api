#!/usr/bin/env python
"""
Script para criar usuário administrador.
Uso: python scripts/create_admin.py
"""

import os
import sys
from getpass import getpass

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from src import create_app
from src.services.service_factory import ServiceFactory


def create_admin():
    """Cria um usuário administrador"""

    print("\n=== Criar Usuário Administrador ===\n")

    # Coletar dados do administrador
    username = input("Nome de usuário: ").strip()
    if not username:
        print("❌ Nome de usuário é obrigatório!")
        return

    email = input("Email: ").strip()
    if not email:
        print("❌ Email é obrigatório!")
        return

    password = getpass("Senha (mínimo 8 caracteres): ")
    if len(password) < 8:
        print("❌ Senha deve ter no mínimo 8 caracteres!")
        return

    password_confirm = getpass("Confirme a senha: ")
    if password != password_confirm:
        print("❌ Senhas não coincidem!")
        return

    auth_service = ServiceFactory.get_auth_service()

    # Verificar se usuário ou email já existem
    if auth_service.get_user_by_username(username):
        print(f"❌ Usuário '{username}' já existe!")
        return

    if auth_service.get_user_by_email(email):
        print(f"❌ Email '{email}' já está cadastrado!")
        return

    # Criar usuário administrador
    user_data = {"username": username, "email": email, "password": password, "role": "admin"}

    user = auth_service.register(user_data)

    if user:
        print(f"\n✅ Administrador criado com sucesso!")
        print(f"   ID: {user['id']}")
        print(f"   Usuário: {user['username']}")
        print(f"   Email: {user['email']}")
        print(f"   Role: {user['role']}")
        print(f"   Criado em: {user['created_at']}")
    else:
        print("\n❌ Erro ao criar administrador!")


if __name__ == "__main__":
    # Criar contexto da aplicação (ambiente via FLASK_ENV)
    app = create_app(os.getenv("FLASK_ENV", "development"))

    with app.app_context():
        try:
            create_admin()
        except KeyboardInterrupt:
            print("\n\n⚠️  Operação cancelada pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
