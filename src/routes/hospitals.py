"""
Rotas para operações com Hospitais.
Blueprint que gerencia endpoints relacionados a hospitais de Angola.
"""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.services.hospital_service import HospitalService
from src.schemas.hospital_schema import HospitalSchema

# Criação do Blueprint para hospitais
hospitals_bp = Blueprint('hospitals', __name__, url_prefix='/hospitals')

# Instância do schema
hospital_schema = HospitalSchema()


@hospitals_bp.route('/all', methods=['GET'])
def get_all_hospitals():
    """
    GET /hospitals/all
    Retorna todos os hospitais de Angola.
    Aceita query parameters: ?provincia_id=<id> ou ?municipio_id=<id>
    """
    provincia_id = request.args.get('provincia_id', type=int)
    municipio_id = request.args.get('municipio_id', type=int)
    
    if municipio_id:
        hospitals = HospitalService.get_by_municipality(municipio_id)
    elif provincia_id:
        hospitals = HospitalService.get_by_province(provincia_id)
    else:
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


@hospitals_bp.route('', methods=['POST'])
def create_hospital():
    """
    POST /hospitals
    Cria um novo hospital.
    """
    try:
        data = hospital_schema.load(request.get_json())
        
        new_hospital = HospitalService.create(data)
        
        if new_hospital:
            return jsonify({
                "success": True,
                "message": "Hospital criado com sucesso",
                "data": new_hospital
            }), 201
        else:
            return jsonify({
                "success": False,
                "message": "Município não pertence à província especificada"
            }), 400
            
    except ValidationError as err:
        return jsonify({
            "success": False,
            "message": "Erro de validação",
            "errors": err.messages
        }), 422
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao criar hospital: {str(e)}"
        }), 500


@hospitals_bp.route('/<int:hospital_id>', methods=['PUT'])
def update_hospital(hospital_id):
    """
    PUT /hospitals/<id>
    Atualiza um hospital existente.
    """
    try:
        data = hospital_schema.load(request.get_json(), partial=True)
        
        updated_hospital = HospitalService.update(hospital_id, data)
        
        if updated_hospital:
            return jsonify({
                "success": True,
                "message": "Hospital atualizado com sucesso",
                "data": updated_hospital
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Hospital não encontrado ou município não pertence à província especificada"
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
            "message": f"Erro ao atualizar hospital: {str(e)}"
        }), 500


@hospitals_bp.route('/<int:hospital_id>', methods=['DELETE'])
def delete_hospital(hospital_id):
    """
    DELETE /hospitals/<id>
    Deleta um hospital.
    """
    try:
        deleted = HospitalService.delete(hospital_id)
        
        if deleted:
            return jsonify({
                "success": True,
                "message": "Hospital deletado com sucesso"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": f"Hospital com ID {hospital_id} não encontrado"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao deletar hospital: {str(e)}"
        }), 500
