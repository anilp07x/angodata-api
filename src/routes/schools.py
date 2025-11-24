"""Rotas para operações com Escolas.
Blueprint que gerencia endpoints relacionados a escolas de Angola.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.schemas.school_schema import SchoolSchema
from src.services.service_factory import ServiceFactory
from src.utils.decorators import editor_or_admin_required

# Criação do Blueprint para escolas
schools_bp = Blueprint("schools", __name__, url_prefix="/schools")

# Instância do schema
school_schema = SchoolSchema()


@schools_bp.route("/all", methods=["GET"])
def get_all_schools():
    """
    GET /schools/all
    Retorna todas as escolas de Angola.
    Aceita query parameters: ?provincia_id=<id> ou ?municipio_id=<id>
    """
    SchoolService = ServiceFactory.get_school_service()
    provincia_id = request.args.get("provincia_id", type=int)
    municipio_id = request.args.get("municipio_id", type=int)

    if municipio_id:
        schools = SchoolService.get_by_municipality(municipio_id)
    elif provincia_id:
        schools = SchoolService.get_by_province(provincia_id)
    else:
        schools = SchoolService.get_all()

    return jsonify({"success": True, "total": len(schools), "data": schools}), 200


@schools_bp.route("/<int:school_id>", methods=["GET"])
def get_school_by_id(school_id):
    """
    GET /schools/<id>
    Retorna uma escola específica por ID.
    """
    SchoolService = ServiceFactory.get_school_service()
    school = SchoolService.get_by_id(school_id)

    if school:
        return jsonify({"success": True, "data": school}), 200
    else:
        return jsonify({"success": False, "message": f"Escola com ID {school_id} não encontrada"}), 404


@schools_bp.route("", methods=["POST"])
@jwt_required()
@editor_or_admin_required()
def create_school():
    """
    POST /schools
    Cria uma nova escola.
    Requer autenticação e role: admin ou editor
    """
    SchoolService = ServiceFactory.get_school_service()
    try:
        data = school_schema.load(request.get_json())

        new_school = SchoolService.create(data)

        if new_school:
            return jsonify({"success": True, "message": "Escola criada com sucesso", "data": new_school}), 201
        else:
            return jsonify({"success": False, "message": "Município não pertence à província especificada"}), 400

    except ValidationError as err:
        return jsonify({"success": False, "message": "Erro de validação", "errors": err.messages}), 422
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao criar escola: {str(e)}"}), 500


@schools_bp.route("/<int:school_id>", methods=["PUT"])
@jwt_required()
@editor_or_admin_required()
def update_school(school_id):
    """
    PUT /schools/<id>
    Atualiza uma escola existente.
    Requer autenticação e role: admin ou editor
    """
    SchoolService = ServiceFactory.get_school_service()
    try:
        data = school_schema.load(request.get_json(), partial=True)

        updated_school = SchoolService.update(school_id, data)

        if updated_school:
            return jsonify({"success": True, "message": "Escola atualizada com sucesso", "data": updated_school}), 200
        else:
            return (
                jsonify(
                    {"success": False, "message": "Escola não encontrada ou município não pertence à província especificada"}
                ),
                404,
            )

    except ValidationError as err:
        return jsonify({"success": False, "message": "Erro de validação", "errors": err.messages}), 422
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao atualizar escola: {str(e)}"}), 500


@schools_bp.route("/<int:school_id>", methods=["DELETE"])
@jwt_required()
@editor_or_admin_required()
def delete_school(school_id):
    """
    DELETE /schools/<id>
    Deleta uma escola.
    Requer autenticação e role: admin ou editor
    """
    SchoolService = ServiceFactory.get_school_service()
    try:
        deleted = SchoolService.delete(school_id)

        if deleted:
            return jsonify({"success": True, "message": "Escola deletada com sucesso"}), 200
        else:
            return jsonify({"success": False, "message": f"Escola com ID {school_id} não encontrada"}), 404

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao deletar escola: {str(e)}"}), 500
