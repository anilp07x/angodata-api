"""
Rotas para operações com Escolas.
Blueprint que gerencia endpoints relacionados a escolas de Angola.
"""

from flask import Blueprint, jsonify
from src.services.school_service import SchoolService

# Criação do Blueprint para escolas
schools_bp = Blueprint('schools', __name__, url_prefix='/schools')


@schools_bp.route('/all', methods=['GET'])
def get_all_schools():
    """
    GET /schools/all
    Retorna todas as escolas de Angola.
    """
    schools = SchoolService.get_all()
    return jsonify({
        "success": True,
        "total": len(schools),
        "data": schools
    }), 200


@schools_bp.route('/<int:school_id>', methods=['GET'])
def get_school_by_id(school_id):
    """
    GET /schools/<id>
    Retorna uma escola específica por ID.
    """
    school = SchoolService.get_by_id(school_id)
    
    if school:
        return jsonify({
            "success": True,
            "data": school
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": f"Escola com ID {school_id} não encontrada"
        }), 404
