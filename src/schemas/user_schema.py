"""
Schema de validação para Usuário
"""

from marshmallow import Schema, ValidationError, fields, validates, validates_schema


class UserRegistrationSchema(Schema):
    """Schema para registro de novo usuário"""

    username = fields.Str(required=True, error_messages={"required": "Campo obrigatório: username"})
    email = fields.Email(required=True, error_messages={"required": "Campo obrigatório: email", "invalid": "Email inválido"})
    password = fields.Str(required=True, error_messages={"required": "Campo obrigatório: password"})
    role = fields.Str(missing="user")  # Default: user

    @validates("username")
    def validate_username(self, value):
        """Valida o username"""
        if not value or len(value.strip()) == 0:
            raise ValidationError("Username não pode estar vazio")
        if len(value) < 3:
            raise ValidationError("Username deve ter no mínimo 3 caracteres")
        if len(value) > 50:
            raise ValidationError("Username deve ter no máximo 50 caracteres")

    @validates("password")
    def validate_password(self, value):
        """Valida a senha"""
        if len(value) < 8:
            raise ValidationError("Senha deve ter no mínimo 8 caracteres")
        if len(value) > 100:
            raise ValidationError("Senha deve ter no máximo 100 caracteres")

    @validates("role")
    def validate_role(self, value):
        """Valida o role"""
        valid_roles = ["admin", "editor", "user"]
        if value not in valid_roles:
            raise ValidationError(f'Role deve ser um dos seguintes: {", ".join(valid_roles)}')


class UserLoginSchema(Schema):
    """Schema para login de usuário"""

    email = fields.Email(required=True, error_messages={"required": "Campo obrigatório: email", "invalid": "Email inválido"})
    password = fields.Str(required=True, error_messages={"required": "Campo obrigatório: password"})


class UserResponseSchema(Schema):
    """Schema para resposta de dados do usuário (sem senha)"""

    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    role = fields.Str()
    created_at = fields.Str()
