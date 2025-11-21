"""
Rotas para operações com Hospitais.
Blueprint que gerencia endpoints relacionados a hospitais de Angola.
"""

from flask import Blueprint, jsonify
from src.services.hospital_service import HospitalService

# Criação do Blueprint para hospitais
hospitals_bp = Blueprint('hospitals', __name__, url_prefix='/hospitals')


@hospitals_bp.route('/all', methods=['GET'])
def get_all_hospitals():
    """
    GET /hospitals/all
    Retorna todos os hospitais de Angola.
    """
    hospitals = HospitalService.get_all()
    return jsonify({
        "success": True,
        "total": len(hospitals),
        "data": hospitals
    }), 200


@hospitals_bp.route('/<int:hospital_id>', methods=['GET'])
def get_hospital_by_id(hospital_id):
    """
    GET /hospitals/<id>
    Retorna um hospital específico por ID.
    """
    hospital = HospitalService.get_by_id(hospital_id)
    
    if hospital:
        return jsonify({
            "success": True,
            "data": hospital
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": f"Hospital com ID {hospital_id} não encontrado"
        }), 404
