"""
Namespaces Swagger para autenticação.
Models alinhados com a API real (AuthService / UserResponseSchema).
"""

from flask_restx import Namespace, fields

# Namespace de autenticação
auth_ns = Namespace("auth", description="Operações de autenticação e gerenciamento de usuários")

# Models de request/response
login_model = auth_ns.model(
    "Login",
    {
        "email": fields.String(required=True, description="Email do usuário", example="anilpedro07@gmail.com"),
        "password": fields.String(required=True, description="Senha do usuário", example="sua-senha"),
    },
)

register_model = auth_ns.model(
    "Register",
    {
        "username": fields.String(
            required=True, description="Nome do usuário (mín 3, máx 50 caracteres)", example="João Silva"
        ),
        "email": fields.String(required=True, description="Email válido", example="joao@example.com"),
        "password": fields.String(
            required=True, description="Senha (mínimo 8, máximo 100 caracteres)", example="senhaForte123"
        ),
        "role": fields.String(description="Role do usuário", enum=["admin", "editor", "user"], default="user"),
    },
)

change_password_model = auth_ns.model(
    "ChangePassword",
    {
        "current_password": fields.String(required=True, description="Senha atual"),
        "new_password": fields.String(required=True, description="Nova senha (mínimo 8 caracteres)"),
    },
)

user_response = auth_ns.model(
    "UserResponse",
    {
        "id": fields.Integer(description="ID do usuário"),
        "username": fields.String(description="Nome do usuário"),
        "email": fields.String(description="Email"),
        "role": fields.String(description="Role do usuário", enum=["admin", "editor", "user"]),
        "created_at": fields.String(description="Data de criação (ISO 8601)"),
    },
)

token_response = auth_ns.model(
    "TokenResponse",
    {
        "access_token": fields.String(description="Token JWT de acesso (validade 24h)"),
        "refresh_token": fields.String(description="Token JWT de renovação (validade 30 dias)"),
        "user": fields.Nested(user_response, description="Dados do usuário autenticado"),
    },
)

success_response = auth_ns.model(
    "SuccessResponse",
    {
        "success": fields.Boolean(description="Status da operação"),
        "message": fields.String(description="Mensagem de retorno"),
        "data": fields.Raw(description="Dados retornados"),
    },
)

error_response = auth_ns.model(
    "ErrorResponse",
    {
        "success": fields.Boolean(description="Status da operação", default=False),
        "message": fields.String(description="Mensagem de erro"),
    },
)
