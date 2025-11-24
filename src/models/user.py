"""
Modelo de dados para Usuários.
Gerencia autenticação e autorização.
"""

# Lista in-memory de usuários (temporário até migração para DB)
USERS = []

# Roles disponíveis no sistema
ROLES = {"admin": "Administrador - acesso total", "editor": "Editor - pode criar e editar", "user": "Usuário - apenas leitura"}
