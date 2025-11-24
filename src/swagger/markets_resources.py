"""
Recursos Swagger para Mercados.
Documentação dos endpoints de markets.
"""

from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required
from src.swagger.markets_ns import (
    markets_ns,
    market_model,
    market_input,
    market_list_response,
    market_response,
    error_response
)
from src.services.service_factory import ServiceFactory
from src.schemas.market_schema import MarketSchema
from src.utils.pagination import PaginationHelper, SearchHelper
from marshmallow import ValidationError
import os

market_schema = MarketSchema()


@markets_ns.route('/all')
class MarketListResource(Resource):
    @markets_ns.doc('list_markets',
        params={
            'page': {'description': 'Número da página (padrão: 1)', 'type': 'int'},
            'per_page': {'description': 'Itens por página (padrão: 20, máximo: 100)', 'type': 'int'},
            'sort_by': {'description': 'Campo para ordenação', 'type': 'string'},
            'order': {'description': 'Ordem: asc ou desc', 'type': 'string', 'enum': ['asc', 'desc']},
            'search': {'description': 'Termo de busca', 'type': 'string'}
        })
    @markets_ns.response(200, 'Sucesso', market_list_response)
    def get(self):
        """Lista todos os mercados com paginação opcional"""
        MarketService = ServiceFactory.get_market_service()
        
        use_pagination = request.args.get('paginate', 'true').lower() == 'true'
        
        if use_pagination:
            page, per_page = PaginationHelper.get_pagination_params()
            markets = MarketService.get_all()
            result = PaginationHelper.paginate_list(markets, page, per_page)
            
            return {
                'success': True,
                'data': result['data'],
                'pagination': result['pagination']
            }, 200
        else:
            markets = MarketService.get_all()
            return {
                'success': True,
                'total': len(markets),
                'data': markets
            }, 200


@markets_ns.route('/<int:id>')
class MarketResource(Resource):
    @markets_ns.doc('get_market')
    @markets_ns.response(200, 'Sucesso', market_response)
    @markets_ns.response(404, 'Mercado não encontrado', error_response)
    def get(self, id):
        """Busca mercado por ID"""
        MarketService = ServiceFactory.get_market_service()
        market = MarketService.get_by_id(id)
        
        if market:
            return {
                'success': True,
                'data': market
            }, 200
        
        return {
            'success': False,
            'message': 'Mercado não encontrado'
        }, 404

    @markets_ns.doc('update_market', security='Bearer')
    @markets_ns.expect(market_input, validate=True)
    @markets_ns.response(200, 'Mercado atualizado com sucesso', market_response)
    @markets_ns.response(400, 'Dados inválidos', error_response)
    @markets_ns.response(401, 'Não autorizado', error_response)
    @markets_ns.response(404, 'Mercado não encontrado', error_response)
    @jwt_required()
    def put(self, id):
        """Atualiza mercado existente (requer autenticação)"""
        if not request.json:
            return {'success': False, 'message': 'Dados inválidos'}, 400
            
        try:
            data = market_schema.load(request.json)
            MarketService = ServiceFactory.get_market_service()
            market = MarketService.get_by_id(id)
            
            if not market:
                return {
                    'success': False,
                    'message': 'Mercado não encontrado'
                }, 404
            
            updated_market = MarketService.update(id, data)
            
            return {
                'success': True,
                'message': 'Mercado atualizado com sucesso',
                'data': updated_market
            }, 200
            
        except ValidationError as e:
            return {
                'success': False,
                'message': 'Dados inválidos',
                'errors': e.messages
            }, 400

    @markets_ns.doc('delete_market', security='Bearer')
    @markets_ns.response(200, 'Mercado removido com sucesso')
    @markets_ns.response(401, 'Não autorizado', error_response)
    @markets_ns.response(404, 'Mercado não encontrado', error_response)
    @jwt_required()
    def delete(self, id):
        """Remove mercado (requer autenticação)"""
        MarketService = ServiceFactory.get_market_service()
        market = MarketService.get_by_id(id)
        
        if not market:
            return {
                'success': False,
                'message': 'Mercado não encontrado'
            }, 404
        
        MarketService.delete(id)
        
        return {
            'success': True,
            'message': 'Mercado removido com sucesso'
        }, 200


@markets_ns.route('')
class MarketCreateResource(Resource):
    @markets_ns.doc('create_market', security='Bearer')
    @markets_ns.expect(market_input, validate=True)
    @markets_ns.response(201, 'Mercado criado com sucesso', market_response)
    @markets_ns.response(400, 'Dados inválidos', error_response)
    @markets_ns.response(401, 'Não autorizado', error_response)
    @jwt_required()
    def post(self):
        """Cria novo mercado (requer autenticação)"""
        if not request.json:
            return {'success': False, 'message': 'Dados inválidos'}, 400
            
        try:
            data = market_schema.load(request.json)
            MarketService = ServiceFactory.get_market_service()
            new_market = MarketService.create(data)
            
            return {
                'success': True,
                'message': 'Mercado criado com sucesso',
                'data': new_market
            }, 201
            
        except ValidationError as e:
            return {
                'success': False,
                'message': 'Dados inválidos',
                'errors': e.messages
            }, 400


@markets_ns.route('/province/<int:province_id>')
class MarketByProvinceResource(Resource):
    @markets_ns.doc('get_markets_by_province')
    @markets_ns.response(200, 'Sucesso', market_list_response)
    def get(self, province_id):
        """Lista mercados por província"""
        MarketService = ServiceFactory.get_market_service()
        markets = MarketService.get_by_province(province_id)
        
        return {
            'success': True,
            'total': len(markets),
            'data': markets
        }, 200
