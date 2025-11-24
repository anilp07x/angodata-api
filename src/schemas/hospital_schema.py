"""
Schema de validação para Hospital
"""

from marshmallow import Schema, ValidationError, fields, validates


class HospitalSchema(Schema):
    """Schema para validação de dados de hospital"""

    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, error_messages={"required": "Campo obrigatório: nome"})
    tipo = fields.Str(required=True, error_messages={"required": "Campo obrigatório: tipo"})
    categoria = fields.Str(required=True, error_messages={"required": "Campo obrigatório: categoria"})
    provincia_id = fields.Int(required=True, error_messages={"required": "Campo obrigatório: provincia_id"})
    provincia_nome = fields.Str(dump_only=True)
    municipio_id = fields.Int(required=True, error_messages={"required": "Campo obrigatório: municipio_id"})
    municipio = fields.Str(dump_only=True)
    endereco = fields.Str(required=True, error_messages={"required": "Campo obrigatório: endereco"})

    @validates("nome")
    def validate_nome(self, value):
        """Valida o nome do hospital"""
        if not value or len(value.strip()) == 0:
            raise ValidationError("Nome não pode estar vazio")
        if len(value) > 200:
            raise ValidationError("Nome deve ter no máximo 200 caracteres")

    @validates("tipo")
    def validate_tipo(self, value):
        """Valida o tipo do hospital"""
        tipos_validos = ["Público", "Privado"]
        if value not in tipos_validos:
            raise ValidationError(f'Tipo deve ser um dos seguintes: {", ".join(tipos_validos)}')

    @validates("categoria")
    def validate_categoria(self, value):
        """Valida a categoria do hospital"""
        categorias_validas = ["Geral", "Central", "Especializado", "Pediátrico"]
        if value not in categorias_validas:
            raise ValidationError(f'Categoria deve ser uma das seguintes: {", ".join(categorias_validas)}')

    @validates("provincia_id")
    def validate_provincia_id(self, value):
        """Valida o ID da província"""
        if value <= 0:
            raise ValidationError("ID da província deve ser um valor positivo")

    @validates("municipio_id")
    def validate_municipio_id(self, value):
        """Valida o ID do município"""
        if value <= 0:
            raise ValidationError("ID do município deve ser um valor positivo")

    @validates("endereco")
    def validate_endereco(self, value):
        """Valida o endereço"""
        if not value or len(value.strip()) == 0:
            raise ValidationError("Endereço não pode estar vazio")
