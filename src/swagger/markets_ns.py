"""
Namespaces Swagger para mercados.
"""

from flask_restx import Namespace, fields

markets_ns = Namespace('markets', description='Operações com mercados de Angola')

market_model = markets_ns.model('Market', {
    'id': fields.Integer(readonly=True, description='ID único do mercado'),
    'nome': fields.String(required=True, description='Nome do mercado'),
    'provincia_id': fields.Integer(required=True, description='ID da província'),
    'provincia_nome': fields.String(readonly=True, description='Nome da província'),
    'tipo': fields.String(description='Tipo de mercado', example='Municipal'),
    'localizacao': fields.String(description='Localização do mercado')
})

market_input = markets_ns.model('MarketInput', {
    'nome': fields.String(required=True, description='Nome do mercado'),
    'provincia_id': fields.Integer(required=True, description='ID da província'),
    'tipo': fields.String(description='Tipo de mercado'),
    'localizacao': fields.String(description='Localização')
})

pagination_metadata = markets_ns.model('PaginationMetadata', {
    'page': fields.Integer(description='Página atual'),
    'per_page': fields.Integer(description='Itens por página'),
    'total_items': fields.Integer(description='Total de itens'),
    'total_pages': fields.Integer(description='Total de páginas'),
    'has_next': fields.Boolean(description='Tem próxima página'),
    'has_prev': fields.Boolean(description='Tem página anterior')
})

market_list_response = markets_ns.model('MarketListResponse', {
    'success': fields.Boolean(description='Status da operação'),
    'total': fields.Integer(description='Total de registros'),
    'data': fields.List(fields.Nested(market_model)),
    'pagination': fields.Nested(pagination_metadata, skip_none=True)
})

market_response = markets_ns.model('MarketResponse', {
    'success': fields.Boolean(description='Status da operação'),
    'data': fields.Nested(market_model)
})

error_response = markets_ns.model('ErrorResponse', {
    'success': fields.Boolean(description='Status da operação', default=False),
    'message': fields.String(description='Mensagem de erro')
})
