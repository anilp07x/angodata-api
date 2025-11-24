"""
Namespaces Swagger para autenticação.
"""

from flask_restx import Namespace, fields

# Namespace de autenticação
auth_ns = Namespace("auth", description="Operações de autenticação e gerenciamento de usuários")

# Models de request/response
login_model = auth_ns.model(
    "Login",
    {
        "email": fields.String(required=True, description="Email do usuário", example="admin@angodata.ao"),
        "password": fields.String(required=True, description="Senha do usuário", example="admin123"),
    },
)

register_model = auth_ns.model(
    "Register",
    {
        "email": fields.String(required=True, description="Email do usuário", example="user@example.com"),
        "password": fields.String(required=True, description="Senha (mínimo 6 caracteres)", example="senha123"),
        "nome": fields.String(required=True, description="Nome completo", example="João Silva"),
        "role": fields.String(description="Role do usuário", enum=["admin", "editor", "user"], default="user"),
    },
)

change_password_model = auth_ns.model(
    "ChangePassword",
    {
        "current_password": fields.String(required=True, description="Senha atual"),
        "new_password": fields.String(required=True, description="Nova senha (mínimo 6 caracteres)"),
    },
)

user_response = auth_ns.model(
    "UserResponse",
    {
        "id": fields.Integer(description="ID do usuário"),
        "email": fields.String(description="Email"),
        "nome": fields.String(description="Nome completo"),
        "role": fields.String(description="Role do usuário"),
        "ativo": fields.Boolean(description="Status ativo"),
        "criado_em": fields.DateTime(description="Data de criação"),
    },
)

token_response = auth_ns.model(
    "TokenResponse",
    {
        "access_token": fields.String(description="Token JWT de acesso"),
        "user": fields.Nested(user_response, description="Dados do usuário"),
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
