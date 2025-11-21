"""
Rotas para operações com Províncias.
Blueprint que gerencia endpoints relacionados a províncias de Angola.
"""

from flask import Blueprint, jsonify
from src.services.province_service import ProvinceService

# Criação do Blueprint para províncias
provinces_bp = Blueprint('provinces', __name__, url_prefix='/provinces')


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
