"""
Rotas para operações com Províncias.
Blueprint que gerencia endpoints relacionados a províncias de Angola.
"""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.services.province_service import ProvinceService
from src.schemas.province_schema import ProvinceSchema

# Criação do Blueprint para províncias
provinces_bp = Blueprint('provinces', __name__, url_prefix='/provinces')

# Instância do schema
province_schema = ProvinceSchema()


@provinces_bp.route('/all', methods=['GET'])
def get_all_provinces():
    """
    GET /provinces/all
    Retorna todas as províncias de Angola.
    """
    provinces = ProvinceService.get_all()
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
def create_province():
    """
    POST /provinces
    Cria uma nova província.
    """
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
def update_province(province_id):
    """
    PUT /provinces/<id>
    Atualiza uma província existente.
    """
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
def delete_province(province_id):
    """
    DELETE /provinces/<id>
    Deleta uma província.
    """
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
