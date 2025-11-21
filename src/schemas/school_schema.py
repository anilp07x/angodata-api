"""
Schema de validação para Escola
"""

from marshmallow import Schema, fields, validates, ValidationError


class SchoolSchema(Schema):
    """Schema para validação de dados de escola"""
    
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, error_messages={
        'required': 'Campo obrigatório: nome'
    })
    tipo = fields.Str(required=True, error_messages={
        'required': 'Campo obrigatório: tipo'
    })
    provincia_id = fields.Int(required=True, error_messages={
        'required': 'Campo obrigatório: provincia_id'
    })
    provincia_nome = fields.Str(dump_only=True)
    municipio_id = fields.Int(required=True, error_messages={
        'required': 'Campo obrigatório: municipio_id'
    })
    municipio = fields.Str(dump_only=True)
    endereco = fields.Str(required=True, error_messages={
        'required': 'Campo obrigatório: endereco'
    })
    
    @validates('nome')
    def validate_nome(self, value):
        """Valida o nome da escola"""
        if not value or len(value.strip()) == 0:
            raise ValidationError('Nome não pode estar vazio')
        if len(value) > 200:
            raise ValidationError('Nome deve ter no máximo 200 caracteres')
    
    @validates('tipo')
    def validate_tipo(self, value):
        """Valida o tipo da escola"""
        tipos_validos = ['Pública', 'Privada']
        if value not in tipos_validos:
            raise ValidationError(f'Tipo deve ser um dos seguintes: {", ".join(tipos_validos)}')
    
    @validates('provincia_id')
    def validate_provincia_id(self, value):
        """Valida o ID da província"""
        if value <= 0:
            raise ValidationError('ID da província deve ser um valor positivo')
    
    @validates('municipio_id')
    def validate_municipio_id(self, value):
        """Valida o ID do município"""
        if value <= 0:
            raise ValidationError('ID do município deve ser um valor positivo')
    
    @validates('endereco')
    def validate_endereco(self, value):
        """Valida o endereço"""
        if not value or len(value.strip()) == 0:
            raise ValidationError('Endereço não pode estar vazio')
