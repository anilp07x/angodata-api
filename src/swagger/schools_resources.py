"""
Recursos Swagger para Escolas.
Documentação dos endpoints de schools.
"""

from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required
from src.swagger.schools_ns import (
    schools_ns,
    school_model,
    school_input,
    school_list_response,
    school_response,
    error_response
)
from src.services.service_factory import ServiceFactory
from src.schemas.school_schema import SchoolSchema
from src.utils.pagination import PaginationHelper, SearchHelper
from marshmallow import ValidationError
import os

school_schema = SchoolSchema()


@schools_ns.route('/all')
class SchoolListResource(Resource):
    @schools_ns.doc('list_schools',
        params={
            'page': {'description': 'Número da página (padrão: 1)', 'type': 'int'},
            'per_page': {'description': 'Itens por página (padrão: 20, máximo: 100)', 'type': 'int'},
            'sort_by': {'description': 'Campo para ordenação', 'type': 'string'},
            'order': {'description': 'Ordem: asc ou desc', 'type': 'string', 'enum': ['asc', 'desc']},
            'search': {'description': 'Termo de busca', 'type': 'string'}
        })
    @schools_ns.response(200, 'Sucesso', school_list_response)
    def get(self):
        """Lista todas as escolas com paginação opcional"""
        SchoolService = ServiceFactory.get_school_service()
        
        use_pagination = request.args.get('paginate', 'true').lower() == 'true'
        
        if use_pagination:
            page, per_page = PaginationHelper.get_pagination_params()
            schools = SchoolService.get_all()
            result = PaginationHelper.paginate_list(schools, page, per_page)
            
            return {
                'success': True,
                'data': result['data'],
                'pagination': result['pagination']
            }, 200
        else:
            schools = SchoolService.get_all()
            return {
                'success': True,
                'total': len(schools),
                'data': schools
            }, 200


@schools_ns.route('/<int:id>')
class SchoolResource(Resource):
    @schools_ns.doc('get_school')
    @schools_ns.response(200, 'Sucesso', school_response)
    @schools_ns.response(404, 'Escola não encontrada', error_response)
    def get(self, id):
        """Busca escola por ID"""
        SchoolService = ServiceFactory.get_school_service()
        school = SchoolService.get_by_id(id)
        
        if school:
            return {
                'success': True,
                'data': school
            }, 200
        
        return {
            'success': False,
            'message': 'Escola não encontrada'
        }, 404

    @schools_ns.doc('update_school', security='Bearer')
    @schools_ns.expect(school_input, validate=True)
    @schools_ns.response(200, 'Escola atualizada com sucesso', school_response)
    @schools_ns.response(400, 'Dados inválidos', error_response)
    @schools_ns.response(401, 'Não autorizado', error_response)
    @schools_ns.response(404, 'Escola não encontrada', error_response)
    @jwt_required()
    def put(self, id):
        """Atualiza escola existente (requer autenticação)"""
        if not request.json:
            return {'success': False, 'message': 'Dados inválidos'}, 400
            
        try:
            data = school_schema.load(request.json)
            SchoolService = ServiceFactory.get_school_service()
            school = SchoolService.get_by_id(id)
            
            if not school:
                return {
                    'success': False,
                    'message': 'Escola não encontrada'
                }, 404
            
            updated_school = SchoolService.update(id, data)
            
            return {
                'success': True,
                'message': 'Escola atualizada com sucesso',
                'data': updated_school
            }, 200
            
        except ValidationError as e:
            return {
                'success': False,
                'message': 'Dados inválidos',
                'errors': e.messages
            }, 400

    @schools_ns.doc('delete_school', security='Bearer')
    @schools_ns.response(200, 'Escola removida com sucesso')
    @schools_ns.response(401, 'Não autorizado', error_response)
    @schools_ns.response(404, 'Escola não encontrada', error_response)
    @jwt_required()
    def delete(self, id):
        """Remove escola (requer autenticação)"""
        SchoolService = ServiceFactory.get_school_service()
        school = SchoolService.get_by_id(id)
        
        if not school:
            return {
                'success': False,
                'message': 'Escola não encontrada'
            }, 404
        
        SchoolService.delete(id)
        
        return {
            'success': True,
            'message': 'Escola removida com sucesso'
        }, 200


@schools_ns.route('')
class SchoolCreateResource(Resource):
    @schools_ns.doc('create_school', security='Bearer')
    @schools_ns.expect(school_input, validate=True)
    @schools_ns.response(201, 'Escola criada com sucesso', school_response)
    @schools_ns.response(400, 'Dados inválidos', error_response)
    @schools_ns.response(401, 'Não autorizado', error_response)
    @jwt_required()
    def post(self):
        """Cria nova escola (requer autenticação)"""
        if not request.json:
            return {'success': False, 'message': 'Dados inválidos'}, 400
            
        try:
            data = school_schema.load(request.json)
            SchoolService = ServiceFactory.get_school_service()
            new_school = SchoolService.create(data)
            
            return {
                'success': True,
                'message': 'Escola criada com sucesso',
                'data': new_school
            }, 201
            
        except ValidationError as e:
            return {
                'success': False,
                'message': 'Dados inválidos',
                'errors': e.messages
            }, 400


@schools_ns.route('/province/<int:province_id>')
class SchoolByProvinceResource(Resource):
    @schools_ns.doc('get_schools_by_province')
    @schools_ns.response(200, 'Sucesso', school_list_response)
    def get(self, province_id):
        """Lista escolas por província"""
        SchoolService = ServiceFactory.get_school_service()
        schools = SchoolService.get_by_province(province_id)
        
        return {
            'success': True,
            'total': len(schools),
            'data': schools
        }, 200
