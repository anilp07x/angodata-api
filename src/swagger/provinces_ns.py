"""
Namespaces Swagger para províncias.
"""

from flask_restx import Namespace, fields

# Namespace de províncias
provinces_ns = Namespace('provinces', description='Operações com províncias de Angola')

# Models
province_model = provinces_ns.model('Province', {
    'id': fields.Integer(readonly=True, description='ID único da província'),
    'nome': fields.String(required=True, description='Nome da província', example='Luanda'),
    'capital': fields.String(required=True, description='Capital da província', example='Luanda'),
    'area_km2': fields.Float(description='Área em km²', example=2417.0),
    'populacao': fields.Integer(description='População estimada', example=6945386)
})

province_input = provinces_ns.model('ProvinceInput', {
    'nome': fields.String(required=True, description='Nome da província', example='Luanda'),
    'capital': fields.String(required=True, description='Capital da província', example='Luanda'),
    'area_km2': fields.Float(description='Área em km²', example=2417.0),
    'populacao': fields.Integer(description='População estimada', example=6945386)
})

pagination_metadata = provinces_ns.model('PaginationMetadata', {
    'page': fields.Integer(description='Página atual'),
    'per_page': fields.Integer(description='Itens por página'),
    'total_items': fields.Integer(description='Total de itens'),
    'total_pages': fields.Integer(description='Total de páginas'),
    'has_next': fields.Boolean(description='Tem próxima página'),
    'has_prev': fields.Boolean(description='Tem página anterior'),
    'next_page': fields.Integer(description='Número da próxima página'),
    'prev_page': fields.Integer(description='Número da página anterior')
})

province_list_response = provinces_ns.model('ProvinceListResponse', {
    'success': fields.Boolean(description='Status da operação'),
    'total': fields.Integer(description='Total de registros'),
    'data': fields.List(fields.Nested(province_model)),
    'pagination': fields.Nested(pagination_metadata, skip_none=True)
})

province_response = provinces_ns.model('ProvinceResponse', {
    'success': fields.Boolean(description='Status da operação'),
    'data': fields.Nested(province_model)
})

bulk_create_input = provinces_ns.model('BulkCreateProvinces', {
    'provinces': fields.List(fields.Nested(province_input), required=True, description='Lista de províncias para criar')
})

bulk_update_item = provinces_ns.model('BulkUpdateItem', {
    'id': fields.Integer(required=True, description='ID da província'),
    'nome': fields.String(description='Nome da província'),
    'capital': fields.String(description='Capital da província'),
    'area_km2': fields.Float(description='Área em km²'),
    'populacao': fields.Integer(description='População')
})

bulk_update_input = provinces_ns.model('BulkUpdateProvinces', {
    'updates': fields.List(fields.Nested(bulk_update_item), required=True, description='Lista de atualizações')
})

bulk_delete_input = provinces_ns.model('BulkDeleteProvinces', {
    'ids': fields.List(fields.Integer, required=True, description='Lista de IDs para deletar', example=[1, 2, 3])
})

bulk_response = provinces_ns.model('BulkOperationResponse', {
    'success': fields.Boolean(description='Status da operação'),
    'message': fields.String(description='Mensagem de retorno'),
    'created': fields.Integer(description='Registros criados'),
    'updated': fields.Integer(description='Registros atualizados'),
    'deleted': fields.Integer(description='Registros deletados'),
    'failed': fields.Integer(description='Operações falhadas'),
    'data': fields.List(fields.Nested(province_model), skip_none=True),
    'ids': fields.List(fields.Integer, skip_none=True),
    'errors': fields.List(fields.String, description='Lista de erros')
})

error_response = provinces_ns.model('ErrorResponse', {
    'success': fields.Boolean(description='Status da operação', default=False),
    'message': fields.String(description='Mensagem de erro')
})
