"""
Schema de validação para Província
"""

from marshmallow import Schema, fields, validates, ValidationError


class ProvinceSchema(Schema):
    """Schema para validação de dados de província"""
    
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, error_messages={
        'required': 'Campo obrigatório: nome'
    })
    capital = fields.Str(required=True, error_messages={
        'required': 'Campo obrigatório: capital'
    })
    area_km2 = fields.Float(required=True, error_messages={
        'required': 'Campo obrigatório: area_km2'
    })
    populacao = fields.Int(required=True, error_messages={
        'required': 'Campo obrigatório: populacao'
    })
    
    @validates('nome')
    def validate_nome(self, value):
        """Valida o nome da província"""
        if not value or len(value.strip()) == 0:
            raise ValidationError('Nome não pode estar vazio')
        if len(value) > 100:
            raise ValidationError('Nome deve ter no máximo 100 caracteres')
    
    @validates('capital')
    def validate_capital(self, value):
        """Valida o nome da capital"""
        if not value or len(value.strip()) == 0:
            raise ValidationError('Capital não pode estar vazia')
        if len(value) > 100:
            raise ValidationError('Capital deve ter no máximo 100 caracteres')
    
    @validates('area_km2')
    def validate_area(self, value):
        """Valida a área"""
        if value <= 0:
            raise ValidationError('Área deve ser um valor positivo')
    
    @validates('populacao')
    def validate_populacao(self, value):
        """Valida a população"""
        if value < 0:
            raise ValidationError('População deve ser um valor positivo ou zero')
