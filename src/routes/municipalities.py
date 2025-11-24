"""Rotas para operações com Municípios.
Blueprint que gerencia endpoints relacionados a municípios de Angola.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.schemas.municipality_schema import MunicipalitySchema
from src.services.service_factory import ServiceFactory
from src.utils.decorators import editor_or_admin_required

# Criação do Blueprint para municípios
municipalities_bp = Blueprint("municipalities", __name__, url_prefix="/municipalities")

# Instância do schema
municipality_schema = MunicipalitySchema()


@municipalities_bp.route("/all", methods=["GET"])
def get_all_municipalities():
    """
    GET /municipalities/all
    Retorna todos os municípios de Angola.
    Aceita query parameter: ?provincia_id=<id>
    """
    MunicipalityService = ServiceFactory.get_municipality_service()
    # Filtrar por província se fornecido
    provincia_id = request.args.get("provincia_id", type=int)

    if provincia_id:
        municipalities = MunicipalityService.get_by_province(provincia_id)
    else:
        municipalities = MunicipalityService.get_all()

    return jsonify({"success": True, "total": len(municipalities), "data": municipalities}), 200


@municipalities_bp.route("/<int:municipality_id>", methods=["GET"])
def get_municipality_by_id(municipality_id):
    """
    GET /municipalities/<id>
    Retorna um município específico por ID.
    """
    MunicipalityService = ServiceFactory.get_municipality_service()
    municipality = MunicipalityService.get_by_id(municipality_id)

    if municipality:
        return jsonify({"success": True, "data": municipality}), 200
    else:
        return jsonify({"success": False, "message": f"Município com ID {municipality_id} não encontrado"}), 404


@municipalities_bp.route("", methods=["POST"])
@jwt_required()
@editor_or_admin_required()
def create_municipality():
    """
    POST /municipalities
    Cria um novo município.
    Requer autenticação e role: admin ou editor
    """
    MunicipalityService = ServiceFactory.get_municipality_service()
    try:
        data = municipality_schema.load(request.get_json())

        new_municipality = MunicipalityService.create(data)

        if new_municipality:
            return jsonify({"success": True, "message": "Município criado com sucesso", "data": new_municipality}), 201
        else:
            return jsonify({"success": False, "message": "ID da província inválido"}), 400

    except ValidationError as err:
        return jsonify({"success": False, "message": "Erro de validação", "errors": err.messages}), 422
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao criar município: {str(e)}"}), 500


@municipalities_bp.route("/<int:municipality_id>", methods=["PUT"])
@jwt_required()
@editor_or_admin_required()
def update_municipality(municipality_id):
    """
    PUT /municipalities/<id>
    Atualiza um município existente.
    Requer autenticação e role: admin ou editor
    """
    MunicipalityService = ServiceFactory.get_municipality_service()
    try:
        data = municipality_schema.load(request.get_json(), partial=True)

        updated_municipality = MunicipalityService.update(municipality_id, data)

        if updated_municipality:
            return jsonify({"success": True, "message": "Município atualizado com sucesso", "data": updated_municipality}), 200
        else:
            return jsonify({"success": False, "message": "Município não encontrado ou ID da província inválido"}), 404

    except ValidationError as err:
        return jsonify({"success": False, "message": "Erro de validação", "errors": err.messages}), 422
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao atualizar município: {str(e)}"}), 500


@municipalities_bp.route("/<int:municipality_id>", methods=["DELETE"])
@jwt_required()
@editor_or_admin_required()
def delete_municipality(municipality_id):
    """
    DELETE /municipalities/<id>
    Deleta um município.
    Requer autenticação e role: admin ou editor
    """
    MunicipalityService = ServiceFactory.get_municipality_service()
    try:
        # Verificar dependências
        deps = MunicipalityService.has_dependencies(municipality_id)

        if deps["total"] > 0:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Não é possível deletar município. Existem dependências (escolas/mercados/hospitais)",
                        "dependencies": deps,
                    }
                ),
                400,
            )

        deleted = MunicipalityService.delete(municipality_id)

        if deleted:
            return jsonify({"success": True, "message": "Município deletado com sucesso"}), 200
        else:
            return jsonify({"success": False, "message": f"Município com ID {municipality_id} não encontrado"}), 404

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao deletar município: {str(e)}"}), 500
