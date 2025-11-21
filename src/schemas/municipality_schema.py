"""
Schema de validação para Município
"""

from marshmallow import Schema, fields, validates, ValidationError


class MunicipalitySchema(Schema):
    """Schema para validação de dados de município"""
    
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, error_messages={
        'required': 'Campo obrigatório: nome'
    })
    provincia_id = fields.Int(required=True, error_messages={
        'required': 'Campo obrigatório: provincia_id'
    })
    provincia_nome = fields.Str(dump_only=True)
    
    @validates('nome')
    def validate_nome(self, value):
        """Valida o nome do município"""
        if not value or len(value.strip()) == 0:
            raise ValidationError('Nome não pode estar vazio')
        if len(value) > 100:
            raise ValidationError('Nome deve ter no máximo 100 caracteres')
    
    @validates('provincia_id')
    def validate_provincia_id(self, value):
        """Valida o ID da província"""
        if value <= 0:
            raise ValidationError('ID da província deve ser um valor positivo')
