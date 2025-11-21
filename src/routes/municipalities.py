"""
Rotas para operações com Municípios.
Blueprint que gerencia endpoints relacionados a municípios de Angola.
"""

from flask import Blueprint, jsonify
from src.services.municipality_service import MunicipalityService

# Criação do Blueprint para municípios
municipalities_bp = Blueprint('municipalities', __name__, url_prefix='/municipalities')


@municipalities_bp.route('/all', methods=['GET'])
def get_all_municipalities():
    """
    GET /municipalities/all
    Retorna todos os municípios de Angola.
    """
    municipalities = MunicipalityService.get_all()
    return jsonify({
        "success": True,
        "total": len(municipalities),
        "data": municipalities
    }), 200


@municipalities_bp.route('/<int:municipality_id>', methods=['GET'])
def get_municipality_by_id(municipality_id):
    """
    GET /municipalities/<id>
    Retorna um município específico por ID.
    """
    municipality = MunicipalityService.get_by_id(municipality_id)
    
    if municipality:
        return jsonify({
            "success": True,
            "data": municipality
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": f"Município com ID {municipality_id} não encontrado"
        }), 404
