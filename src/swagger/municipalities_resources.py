"""
Recursos Swagger para Municípios.
Documentação dos endpoints de municipalities.
"""

from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required
from src.swagger.municipalities_ns import (
    municipalities_ns,
    municipality_model,
    municipality_input,
    municipality_list_response,
    municipality_response,
    error_response
)
from src.services.service_factory import ServiceFactory
from src.schemas.municipality_schema import MunicipalitySchema
from src.utils.pagination import PaginationHelper, SearchHelper
from marshmallow import ValidationError
import os

municipality_schema = MunicipalitySchema()


@municipalities_ns.route('/all')
class MunicipalityListResource(Resource):
    @municipalities_ns.doc('list_municipalities',
        params={
            'page': {'description': 'Número da página (padrão: 1)', 'type': 'int'},
            'per_page': {'description': 'Itens por página (padrão: 20, máximo: 100)', 'type': 'int'},
            'sort_by': {'description': 'Campo para ordenação', 'type': 'string'},
            'order': {'description': 'Ordem: asc ou desc', 'type': 'string', 'enum': ['asc', 'desc']},
            'search': {'description': 'Termo de busca', 'type': 'string'}
        })
    @municipalities_ns.response(200, 'Sucesso', municipality_list_response)
    def get(self):
        """Lista todos os municípios com paginação opcional"""
        MunicipalityService = ServiceFactory.get_municipality_service()
        
        use_pagination = request.args.get('paginate', 'true').lower() == 'true'
        
        if use_pagination:
            page, per_page = PaginationHelper.get_pagination_params()
            municipalities = MunicipalityService.get_all()
            result = PaginationHelper.paginate_list(municipalities, page, per_page)
            
            return {
                'success': True,
                'data': result['data'],
                'pagination': result['pagination']
            }, 200
        else:
            municipalities = MunicipalityService.get_all()
            return {
                'success': True,
                'total': len(municipalities),
                'data': municipalities
            }, 200


@municipalities_ns.route('/<int:id>')
@municipalities_ns.param('id', 'ID do município')
class MunicipalityResource(Resource):
    @municipalities_ns.doc('get_municipality')
    @municipalities_ns.response(200, 'Sucesso', municipality_response)
    @municipalities_ns.response(404, 'Município não encontrado', error_response)
    def get(self, id):
        """Busca município por ID"""
        MunicipalityService = ServiceFactory.get_municipality_service()
        municipality = MunicipalityService.get_by_id(id)
        
        if not municipality:
            return {
                'success': False,
                'message': f'Município com ID {id} não encontrado'
            }, 404
        
        return {
            'success': True,
            'data': municipality
        }, 200
    
    @municipalities_ns.doc('update_municipality', security='Bearer')
    @municipalities_ns.expect(municipality_input)
    @municipalities_ns.response(200, 'Município atualizado', municipality_response)
    @municipalities_ns.response(404, 'Município não encontrado', error_response)
    @municipalities_ns.response(401, 'Não autorizado', error_response)
    @jwt_required()
    def put(self, id):
        """Atualiza município (requer autenticação Editor ou Admin)"""
        MunicipalityService = ServiceFactory.get_municipality_service()
        
        if not request.json:
            return {
                'success': False,
                'message': 'Dados não fornecidos'
            }, 400
        
        try:
            data = municipality_schema.load(request.json)
        except ValidationError as err:
            return {
                'success': False,
                'message': 'Dados inválidos',
                'errors': err.messages
            }, 400
        
        # Atualizar município
        updated = MunicipalityService.update(id, data)
        
        if not updated:
            return {
                'success': False,
                'message': f'Município com ID {id} não encontrado'
            }, 404
        
        return {
            'success': True,
            'message': 'Município atualizado com sucesso',
            'data': updated
        }, 200
    
    @municipalities_ns.doc('delete_municipality', security='Bearer')
    @municipalities_ns.response(200, 'Município deletado')
    @municipalities_ns.response(404, 'Município não encontrado', error_response)
    @municipalities_ns.response(401, 'Não autorizado', error_response)
    @jwt_required()
    def delete(self, id):
        """Deleta município (requer autenticação Admin)"""
        MunicipalityService = ServiceFactory.get_municipality_service()
        
        if MunicipalityService.delete(id):
            return {
                'success': True,
                'message': f'Município ID {id} deletado com sucesso'
            }, 200
        
        return {
            'success': False,
            'message': f'Município com ID {id} não encontrado'
        }, 404


@municipalities_ns.route('')
class MunicipalityCreateResource(Resource):
    @municipalities_ns.doc('create_municipality', security='Bearer')
    @municipalities_ns.expect(municipality_input)
    @municipalities_ns.response(201, 'Município criado', municipality_response)
    @municipalities_ns.response(400, 'Dados inválidos', error_response)
    @municipalities_ns.response(401, 'Não autorizado', error_response)
    @jwt_required()
    def post(self):
        """Cria novo município (requer autenticação Editor ou Admin)"""
        MunicipalityService = ServiceFactory.get_municipality_service()
        
        if not request.json:
            return {
                'success': False,
                'message': 'Dados não fornecidos'
            }, 400
        
        try:
            data = municipality_schema.load(request.json)
        except ValidationError as err:
            return {
                'success': False,
                'message': 'Dados inválidos',
                'errors': err.messages
            }, 400
        
        new_municipality = MunicipalityService.create(data)
        
        return {
            'success': True,
            'message': 'Município criado com sucesso',
            'data': new_municipality
        }, 201


@municipalities_ns.route('/province/<int:province_id>')
@municipalities_ns.param('province_id', 'ID da província')
class MunicipalityByProvinceResource(Resource):
    @municipalities_ns.doc('get_municipalities_by_province')
    @municipalities_ns.response(200, 'Sucesso', municipality_list_response)
    @municipalities_ns.response(404, 'Província não encontrada', error_response)
    def get(self, province_id):
        """Lista municípios de uma província específica"""
        MunicipalityService = ServiceFactory.get_municipality_service()
        municipalities = MunicipalityService.get_by_province(province_id)
        
        if not municipalities:
            return {
                'success': False,
                'message': f'Nenhum município encontrado para província ID {province_id}'
            }, 404
        
        return {
            'success': True,
            'total': len(municipalities),
            'data': municipalities
        }, 200
