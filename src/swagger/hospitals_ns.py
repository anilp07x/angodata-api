"""
Namespaces Swagger para hospitais.
"""

from flask_restx import Namespace, fields

hospitals_ns = Namespace('hospitals', description='Operações com hospitais de Angola')

hospital_model = hospitals_ns.model('Hospital', {
    'id': fields.Integer(readonly=True, description='ID único do hospital'),
    'nome': fields.String(required=True, description='Nome do hospital'),
    'provincia_id': fields.Integer(required=True, description='ID da província'),
    'provincia_nome': fields.String(readonly=True, description='Nome da província'),
    'tipo': fields.String(description='Tipo de hospital', example='Geral'),
    'localizacao': fields.String(description='Localização do hospital'),
    'capacidade': fields.Integer(description='Capacidade de leitos')
})

hospital_input = hospitals_ns.model('HospitalInput', {
    'nome': fields.String(required=True, description='Nome do hospital'),
    'provincia_id': fields.Integer(required=True, description='ID da província'),
    'tipo': fields.String(description='Tipo de hospital'),
    'localizacao': fields.String(description='Localização'),
    'capacidade': fields.Integer(description='Capacidade de leitos')
})

pagination_metadata = hospitals_ns.model('PaginationMetadata', {
    'page': fields.Integer(description='Página atual'),
    'per_page': fields.Integer(description='Itens por página'),
    'total_items': fields.Integer(description='Total de itens'),
    'total_pages': fields.Integer(description='Total de páginas'),
    'has_next': fields.Boolean(description='Tem próxima página'),
    'has_prev': fields.Boolean(description='Tem página anterior')
})

hospital_list_response = hospitals_ns.model('HospitalListResponse', {
    'success': fields.Boolean(description='Status da operação'),
    'total': fields.Integer(description='Total de registros'),
    'data': fields.List(fields.Nested(hospital_model)),
    'pagination': fields.Nested(pagination_metadata, skip_none=True)
})

hospital_response = hospitals_ns.model('HospitalResponse', {
    'success': fields.Boolean(description='Status da operação'),
    'data': fields.Nested(hospital_model)
})

error_response = hospitals_ns.model('ErrorResponse', {
    'success': fields.Boolean(description='Status da operação', default=False),
    'message': fields.String(description='Mensagem de erro')
})
