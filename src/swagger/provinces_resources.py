"""
Recursos Swagger para Províncias.
Documentação dos endpoints existentes em /provinces.
"""

from flask_restx import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.swagger.provinces_ns import (
    provinces_ns, 
    province_list_response,
    province_response,
    province_input,
    error_response,
    bulk_create_input,
    bulk_update_input,
    bulk_delete_input,
    bulk_response
)
from src.services.service_factory import ServiceFactory
from src.schemas.province_schema import ProvinceSchema
from src.utils.pagination import PaginationHelper, SearchHelper
from marshmallow import ValidationError
import os

province_schema = ProvinceSchema()


@provinces_ns.route('/all')
class ProvinceListResource(Resource):
    @provinces_ns.doc('list_provinces',
        params={
            'page': {'description': 'Número da página (padrão: 1)', 'type': 'int'},
            'per_page': {'description': 'Itens por página (padrão: 20, máximo: 100)', 'type': 'int'},
            'sort_by': {'description': 'Campo para ordenação (ex: nome)', 'type': 'string'},
            'order': {'description': 'Ordem: asc ou desc (padrão: asc)', 'type': 'string', 'enum': ['asc', 'desc']},
            'search': {'description': 'Termo de busca em nome ou capital', 'type': 'string'},
            'paginate': {'description': 'Usar paginação (true/false, padrão: true)', 'type': 'boolean'}
        })
    @provinces_ns.response(200, 'Sucesso', province_list_response)
    @provinces_ns.response(500, 'Erro interno', error_response)
    def get(self):
        """Lista todas as províncias com paginação e busca opcional"""
        ProvinceService = ServiceFactory.get_province_service()
        
        use_pagination = request.args.get('paginate', 'true').lower() == 'true'
        use_database = os.getenv('USE_DATABASE', 'False').lower() == 'true'
        
        if use_pagination and use_database and hasattr(ProvinceService, 'get_all_paginated'):
            page, per_page = PaginationHelper.get_pagination_params()
            sort_by, order = SearchHelper.get_sort_params()
            search = SearchHelper.get_search_query()
            
            result = ProvinceService.get_all_paginated(
                page=page,
                per_page=per_page,
                sort_by=sort_by,
                order=order,
                search=search
            )
            
            return {
                'success': True,
                'data': result['data'],
                'pagination': result['pagination']
            }, 200
        elif use_pagination:
            page, per_page = PaginationHelper.get_pagination_params()
            provinces = ProvinceService.get_all()
            result = PaginationHelper.paginate_list(provinces, page, per_page)
            
            return {
                'success': True,
                'data': result['data'],
                'pagination': result['pagination']
            }, 200
        else:
            provinces = ProvinceService.get_all()
            return {
                'success': True,
                'total': len(provinces),
                'data': provinces
            }, 200


@provinces_ns.route('/<int:id>')
@provinces_ns.param('id', 'ID da província')
class ProvinceResource(Resource):
    @provinces_ns.doc('get_province')
    @provinces_ns.response(200, 'Sucesso', province_response)
    @provinces_ns.response(404, 'Província não encontrada', error_response)
    def get(self, id):
        """Busca província por ID"""
        ProvinceService = ServiceFactory.get_province_service()
        province = ProvinceService.get_by_id(id)
        
        if not province:
            return {
                'success': False,
                'message': f'Província com ID {id} não encontrada'
            }, 404
        
        return {
            'success': True,
            'data': province
        }, 200
    
    @provinces_ns.doc('update_province', security='Bearer')
    @provinces_ns.expect(province_input)
    @provinces_ns.response(200, 'Província atualizada com sucesso', province_response)
    @provinces_ns.response(404, 'Província não encontrada', error_response)
    @provinces_ns.response(401, 'Não autorizado', error_response)
    @jwt_required()
    def put(self, id):
        """Atualiza província existente (requer autenticação Editor ou Admin)"""
        ProvinceService = ServiceFactory.get_province_service()
        
        if not request.json:
            return {
                'success': False,
                'message': 'Dados não fornecidos'
            }, 400
        
        try:
            data = province_schema.load(request.json)
        except ValidationError as err:
            return {
                'success': False,
                'message': 'Dados inválidos',
                'errors': err.messages
            }, 400
        
        updated = ProvinceService.update(id, data)
        
        if not updated:
            return {
                'success': False,
                'message': f'Província com ID {id} não encontrada'
            }, 404
        
        return {
            'success': True,
            'message': 'Província atualizada com sucesso',
            'data': updated
        }, 200
    
    @provinces_ns.doc('delete_province', security='Bearer')
    @provinces_ns.response(200, 'Província deletada com sucesso')
    @provinces_ns.response(404, 'Província não encontrada', error_response)
    @provinces_ns.response(401, 'Não autorizado', error_response)
    @jwt_required()
    def delete(self, id):
        """Deleta província (requer autenticação Admin)"""
        ProvinceService = ServiceFactory.get_province_service()
        
        if ProvinceService.delete(id):
            return {
                'success': True,
                'message': f'Província ID {id} deletada com sucesso'
            }, 200
        
        return {
            'success': False,
            'message': f'Província com ID {id} não encontrada'
        }, 404


@provinces_ns.route('')
class ProvinceCreateResource(Resource):
    @provinces_ns.doc('create_province', security='Bearer')
    @provinces_ns.expect(province_input)
    @provinces_ns.response(201, 'Província criada com sucesso', province_response)
    @provinces_ns.response(400, 'Dados inválidos', error_response)
    @provinces_ns.response(401, 'Não autorizado', error_response)
    @jwt_required()
    def post(self):
        """Cria nova província (requer autenticação Editor ou Admin)"""
        ProvinceService = ServiceFactory.get_province_service()
        
        if not request.json:
            return {
                'success': False,
                'message': 'Dados não fornecidos'
            }, 400
        
        try:
            data = province_schema.load(request.json)
        except ValidationError as err:
            return {
                'success': False,
                'message': 'Dados inválidos',
                'errors': err.messages
            }, 400
        
        new_province = ProvinceService.create(data)
        
        return {
            'success': True,
            'message': 'Província criada com sucesso',
            'data': new_province
        }, 201


@provinces_ns.route('/bulk/create')
class ProvinceBulkCreateResource(Resource):
    @provinces_ns.doc('bulk_create_provinces', security='Bearer')
    @provinces_ns.expect(bulk_create_input)
    @provinces_ns.response(201, 'Províncias criadas com sucesso', bulk_response)
    @provinces_ns.response(401, 'Não autorizado', error_response)
    @jwt_required()
    def post(self):
        """Cria múltiplas províncias de uma vez (requer autenticação Editor ou Admin)"""
        ProvinceService = ServiceFactory.get_province_service()
        data = request.json
        
        if not data or 'provinces' not in data:
            return {
                'success': False,
                'message': 'Formato inválido. Esperado: {provinces: [...]}'
            }, 400
        
        if not hasattr(ProvinceService, 'bulk_create'):
            return {
                'success': False,
                'message': 'Operação bulk não disponível no modo atual'
            }, 400
        
        result = ProvinceService.bulk_create(data['provinces'])
        
        return {
            'success': True,
            'message': f"{result['created']} províncias criadas com sucesso",
            **result
        }, 201
