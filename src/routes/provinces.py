"""
Rotas para operações com Províncias.
Blueprint que gerencia endpoints relacionados a províncias de Angola.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from src.services.service_factory import ServiceFactory
from src.schemas.province_schema import ProvinceSchema
from src.utils.decorators import editor_or_admin_required
from src.utils.audit import audit_log
from src.utils.pagination import PaginationHelper, SearchHelper
from src.utils.cache import cached_route, invalidate_entity_cache
import os

# Criação do Blueprint para províncias
provinces_bp = Blueprint('provinces', __name__, url_prefix='/provinces')

# Instância do schema
province_schema = ProvinceSchema()


@provinces_bp.route('/all', methods=['GET'])
@cached_route(timeout=300)
def get_all_provinces():
    """
    GET /provinces/all
    Retorna todas as províncias de Angola.
    
    Query params:
    - page: Número da página (default: 1)
    - per_page: Itens por página (default: 20, max: 100)
    - sort_by: Campo para ordenar (default: nome)
    - order: asc ou desc (default: asc)
    - search: Termo de busca em nome ou capital
    """
    ProvinceService = ServiceFactory.get_province_service()
    
    # Verificar se deve usar paginação
    use_pagination = request.args.get('paginate', 'true').lower() == 'true'
    use_database = os.getenv('USE_DATABASE', 'False').lower() == 'true'
    
    if use_pagination and use_database and hasattr(ProvinceService, 'get_all_paginated'):
        # Obter parâmetros de paginação e busca
        page, per_page = PaginationHelper.get_pagination_params()
        sort_by, order = SearchHelper.get_sort_params()
        search = SearchHelper.get_search_query()
        
        # Buscar paginado
        result = ProvinceService.get_all_paginated(
            page=page,
            per_page=per_page,
            sort_by=sort_by or 'nome',
            order=order,
            search=search
        )
        
        return jsonify({
            "success": True,
            **result
        }), 200
    else:
        # Buscar sem paginação (modo legado)
        provinces = ProvinceService.get_all()
        
        # Se for modo JSON e pediu paginação, aplicar manualmente
        if use_pagination and not use_database:
            page, per_page = PaginationHelper.get_pagination_params()
            result = PaginationHelper.paginate_list(provinces, page, per_page)
            return jsonify({
                "success": True,
                **result
            }), 200
        
        return jsonify({
            "success": True,
            "total": len(provinces),
            "data": provinces
        }), 200


@provinces_bp.route('/<int:province_id>', methods=['GET'])
def get_province_by_id(province_id):
    """
    GET /provinces/<id>
    Retorna uma província específica por ID.
    """
    ProvinceService = ServiceFactory.get_province_service()
    province = ProvinceService.get_by_id(province_id)
    
    if province:
        return jsonify({
            "success": True,
            "data": province
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": f"Província com ID {province_id} não encontrada"
        }), 404


@provinces_bp.route('', methods=['POST'])
@jwt_required()
@editor_or_admin_required()
@audit_log('CREATE', 'province')
def create_province():
    """
    POST /provinces
    Cria uma nova província.
    """
    ProvinceService = ServiceFactory.get_province_service()
    try:
        # Validar dados de entrada
        data = province_schema.load(request.get_json())
        
        # Criar província
        new_province = ProvinceService.create(data)
        
        return jsonify({
            "success": True,
            "message": "Província criada com sucesso",
            "data": new_province
        }), 201
        
    except ValidationError as err:
        return jsonify({
            "success": False,
            "message": "Erro de validação",
            "errors": err.messages
        }), 422
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao criar província: {str(e)}"
        }), 500


@provinces_bp.route('/<int:province_id>', methods=['PUT'])
@jwt_required()
@editor_or_admin_required()
@audit_log('UPDATE', 'province')
def update_province(province_id):
    """
    PUT /provinces/<id>
    Atualiza uma província existente.
    """
    ProvinceService = ServiceFactory.get_province_service()
    try:
        # Validar dados de entrada (partial=True para permitir updates parciais)
        data = province_schema.load(request.get_json(), partial=True)
        
        # Atualizar província
        updated_province = ProvinceService.update(province_id, data)
        
        if updated_province:
            return jsonify({
                "success": True,
                "message": "Província atualizada com sucesso",
                "data": updated_province
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": f"Província com ID {province_id} não encontrada"
            }), 404
            
    except ValidationError as err:
        return jsonify({
            "success": False,
            "message": "Erro de validação",
            "errors": err.messages
        }), 422
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao atualizar província: {str(e)}"
        }), 500


@provinces_bp.route('/<int:province_id>', methods=['DELETE'])
@jwt_required()
@editor_or_admin_required()
@audit_log('DELETE', 'province')
def delete_province(province_id):
    """
    DELETE /provinces/<id>
    Deleta uma província.
    """
    ProvinceService = ServiceFactory.get_province_service()
    try:
        # Verificar se tem municípios associados
        municipality_count = ProvinceService.has_municipalities(province_id)
        
        if municipality_count > 0:
            return jsonify({
                "success": False,
                "message": f"Não é possível deletar província. Existem {municipality_count} municípios associados"
            }), 400
        
        # Deletar província
        deleted = ProvinceService.delete(province_id)
        
        if deleted:
            # Invalidar cache
            invalidate_entity_cache('provinces')
            
            return jsonify({
                "success": True,
                "message": "Província deletada com sucesso"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": f"Província com ID {province_id} não encontrada"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao deletar província: {str(e)}"
        }), 500


@provinces_bp.route('/bulk', methods=['POST'])
@jwt_required()
@editor_or_admin_required()
@audit_log('BULK_CREATE', 'province')
def bulk_create_provinces():
    """
    POST /provinces/bulk
    Cria múltiplas províncias de uma vez.
    Requer autenticação e role: admin ou editor
    
    Body: {"provinces": [{...}, {...}]}
    """
    ProvinceService = ServiceFactory.get_province_service()
    
    # Verificar se service suporta bulk operations
    if not hasattr(ProvinceService, 'bulk_create'):
        return jsonify({
            "success": False,
            "message": "Bulk operations não disponíveis no modo atual (use USE_DATABASE=True)"
        }), 400
    
    try:
        data = request.get_json()
        provinces_data = data.get('provinces', [])
        
        if not provinces_data:
            return jsonify({
                "success": False,
                "message": "Lista de províncias vazia"
            }), 400
        
        # Validar cada província
        validated = []
        for prov_data in provinces_data:
            try:
                validated_prov = province_schema.load(prov_data)
                validated.append(validated_prov)
            except ValidationError as err:
                return jsonify({
                    "success": False,
                    "message": "Erro de validação em uma das províncias",
                    "errors": err.messages,
                    "data": prov_data
                }), 422
        
        # Criar em bulk
        result = ProvinceService.bulk_create(validated)
        
        # Invalidar cache
        if result['created'] > 0:
            invalidate_entity_cache('provinces')
        
        return jsonify({
            "success": True,
            "message": f"{result['created']} províncias criadas, {result['failed']} falharam",
            **result
        }), 201 if result['created'] > 0 else 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao criar províncias em bulk: {str(e)}"
        }), 500


@provinces_bp.route('/bulk', methods=['PUT'])
@jwt_required()
@editor_or_admin_required()
@audit_log('BULK_UPDATE', 'province')
def bulk_update_provinces():
    """
    PUT /provinces/bulk
    Atualiza múltiplas províncias de uma vez.
    Requer autenticação e role: admin ou editor
    
    Body: {"updates": [{"id": 1, "nome": "..."}, ...]}
    """
    ProvinceService = ServiceFactory.get_province_service()
    
    if not hasattr(ProvinceService, 'bulk_update'):
        return jsonify({
            "success": False,
            "message": "Bulk operations não disponíveis no modo atual (use USE_DATABASE=True)"
        }), 400
    
    try:
        data = request.get_json()
        updates = data.get('updates', [])
        
        if not updates:
            return jsonify({
                "success": False,
                "message": "Lista de atualizações vazia"
            }), 400
        
        # Atualizar em bulk
        result = ProvinceService.bulk_update(updates)
        
        # Invalidar cache
        if result['updated'] > 0:
            invalidate_entity_cache('provinces')
        
        return jsonify({
            "success": True,
            "message": f"{result['updated']} províncias atualizadas, {result['failed']} falharam",
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao atualizar províncias em bulk: {str(e)}"
        }), 500


@provinces_bp.route('/bulk', methods=['DELETE'])
@jwt_required()
@editor_or_admin_required()
@audit_log('BULK_DELETE', 'province')
def bulk_delete_provinces():
    """
    DELETE /provinces/bulk
    Deleta múltiplas províncias de uma vez.
    Requer autenticação e role: admin ou editor
    
    Body: {"ids": [1, 2, 3]}
    """
    ProvinceService = ServiceFactory.get_province_service()
    
    if not hasattr(ProvinceService, 'bulk_delete'):
        return jsonify({
            "success": False,
            "message": "Bulk operations não disponíveis no modo atual (use USE_DATABASE=True)"
        }), 400
    
    try:
        data = request.get_json()
        province_ids = data.get('ids', [])
        
        if not province_ids:
            return jsonify({
                "success": False,
                "message": "Lista de IDs vazia"
            }), 400
        
        # Deletar em bulk
        result = ProvinceService.bulk_delete(province_ids)
        
        # Invalidar cache
        if result['deleted'] > 0:
            invalidate_entity_cache('provinces')
        
        return jsonify({
            "success": True,
            "message": f"{result['deleted']} províncias deletadas, {result['failed']} falharam",
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao deletar províncias em bulk: {str(e)}"
        }), 500
