"""
Namespaces Swagger para municípios.
"""

from flask_restx import Namespace, fields

# Namespace de municípios
municipalities_ns = Namespace('municipalities', description='Operações com municípios de Angola')

# Models
municipality_model = municipalities_ns.model('Municipality', {
    'id': fields.Integer(readonly=True, description='ID único do município'),
    'nome': fields.String(required=True, description='Nome do município', example='Luanda'),
    'provincia_id': fields.Integer(required=True, description='ID da província', example=1),
    'provincia_nome': fields.String(readonly=True, description='Nome da província')
})

municipality_input = municipalities_ns.model('MunicipalityInput', {
    'nome': fields.String(required=True, description='Nome do município', example='Luanda'),
    'provincia_id': fields.Integer(required=True, description='ID da província', example=1)
})

pagination_metadata = municipalities_ns.model('PaginationMetadata', {
    'page': fields.Integer(description='Página atual'),
    'per_page': fields.Integer(description='Itens por página'),
    'total_items': fields.Integer(description='Total de itens'),
    'total_pages': fields.Integer(description='Total de páginas'),
    'has_next': fields.Boolean(description='Tem próxima página'),
    'has_prev': fields.Boolean(description='Tem página anterior')
})

municipality_list_response = municipalities_ns.model('MunicipalityListResponse', {
    'success': fields.Boolean(description='Status da operação'),
    'total': fields.Integer(description='Total de registros'),
    'data': fields.List(fields.Nested(municipality_model)),
    'pagination': fields.Nested(pagination_metadata, skip_none=True)
})

municipality_response = municipalities_ns.model('MunicipalityResponse', {
    'success': fields.Boolean(description='Status da operação'),
    'data': fields.Nested(municipality_model)
})

error_response = municipalities_ns.model('ErrorResponse', {
    'success': fields.Boolean(description='Status da operação', default=False),
    'message': fields.String(description='Mensagem de erro')
})
