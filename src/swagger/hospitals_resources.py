"""
Recursos Swagger para Hospitais.
Documentação dos endpoints de hospitals.
"""

import os

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from marshmallow import ValidationError

from src.schemas.hospital_schema import HospitalSchema
from src.services.service_factory import ServiceFactory
from src.swagger.hospitals_ns import (
    error_response,
    hospital_input,
    hospital_list_response,
    hospital_model,
    hospital_response,
    hospitals_ns,
)
from src.utils.pagination import PaginationHelper, SearchHelper

hospital_schema = HospitalSchema()


@hospitals_ns.route("/all")
class HospitalListResource(Resource):
    @hospitals_ns.doc(
        "list_hospitals",
        params={
            "page": {"description": "Número da página (padrão: 1)", "type": "int"},
            "per_page": {"description": "Itens por página (padrão: 20, máximo: 100)", "type": "int"},
            "sort_by": {"description": "Campo para ordenação", "type": "string"},
            "order": {"description": "Ordem: asc ou desc", "type": "string", "enum": ["asc", "desc"]},
            "search": {"description": "Termo de busca", "type": "string"},
        },
    )
    @hospitals_ns.response(200, "Sucesso", hospital_list_response)
    def get(self):
        """Lista todos os hospitais com paginação opcional"""
        HospitalService = ServiceFactory.get_hospital_service()

        use_pagination = request.args.get("paginate", "true").lower() == "true"

        if use_pagination:
            page, per_page = PaginationHelper.get_pagination_params()
            hospitals = HospitalService.get_all()
            result = PaginationHelper.paginate_list(hospitals, page, per_page)

            return {"success": True, "data": result["data"], "pagination": result["pagination"]}, 200
        else:
            hospitals = HospitalService.get_all()
            return {"success": True, "total": len(hospitals), "data": hospitals}, 200


@hospitals_ns.route("/<int:id>")
class HospitalResource(Resource):
    @hospitals_ns.doc("get_hospital")
    @hospitals_ns.response(200, "Sucesso", hospital_response)
    @hospitals_ns.response(404, "Hospital não encontrado", error_response)
    def get(self, id):
        """Busca hospital por ID"""
        HospitalService = ServiceFactory.get_hospital_service()
        hospital = HospitalService.get_by_id(id)

        if hospital:
            return {"success": True, "data": hospital}, 200

        return {"success": False, "message": "Hospital não encontrado"}, 404

    @hospitals_ns.doc("update_hospital", security="Bearer")
    @hospitals_ns.expect(hospital_input, validate=True)
    @hospitals_ns.response(200, "Hospital atualizado com sucesso", hospital_response)
    @hospitals_ns.response(400, "Dados inválidos", error_response)
    @hospitals_ns.response(401, "Não autorizado", error_response)
    @hospitals_ns.response(404, "Hospital não encontrado", error_response)
    @jwt_required()
    def put(self, id):
        """Atualiza hospital existente (requer autenticação)"""
        if not request.json:
            return {"success": False, "message": "Dados inválidos"}, 400

        try:
            data = hospital_schema.load(request.json)
            HospitalService = ServiceFactory.get_hospital_service()
            hospital = HospitalService.get_by_id(id)

            if not hospital:
                return {"success": False, "message": "Hospital não encontrado"}, 404

            updated_hospital = HospitalService.update(id, data)

            return {"success": True, "message": "Hospital atualizado com sucesso", "data": updated_hospital}, 200

        except ValidationError as e:
            return {"success": False, "message": "Dados inválidos", "errors": e.messages}, 400

    @hospitals_ns.doc("delete_hospital", security="Bearer")
    @hospitals_ns.response(200, "Hospital removido com sucesso")
    @hospitals_ns.response(401, "Não autorizado", error_response)
    @hospitals_ns.response(404, "Hospital não encontrado", error_response)
    @jwt_required()
    def delete(self, id):
        """Remove hospital (requer autenticação)"""
        HospitalService = ServiceFactory.get_hospital_service()
        hospital = HospitalService.get_by_id(id)

        if not hospital:
            return {"success": False, "message": "Hospital não encontrado"}, 404

        HospitalService.delete(id)

        return {"success": True, "message": "Hospital removido com sucesso"}, 200


@hospitals_ns.route("")
class HospitalCreateResource(Resource):
    @hospitals_ns.doc("create_hospital", security="Bearer")
    @hospitals_ns.expect(hospital_input, validate=True)
    @hospitals_ns.response(201, "Hospital criado com sucesso", hospital_response)
    @hospitals_ns.response(400, "Dados inválidos", error_response)
    @hospitals_ns.response(401, "Não autorizado", error_response)
    @jwt_required()
    def post(self):
        """Cria novo hospital (requer autenticação)"""
        if not request.json:
            return {"success": False, "message": "Dados inválidos"}, 400

        try:
            data = hospital_schema.load(request.json)
            HospitalService = ServiceFactory.get_hospital_service()
            new_hospital = HospitalService.create(data)

            return {"success": True, "message": "Hospital criado com sucesso", "data": new_hospital}, 201

        except ValidationError as e:
            return {"success": False, "message": "Dados inválidos", "errors": e.messages}, 400


@hospitals_ns.route("/province/<int:province_id>")
class HospitalByProvinceResource(Resource):
    @hospitals_ns.doc("get_hospitals_by_province")
    @hospitals_ns.response(200, "Sucesso", hospital_list_response)
    def get(self, province_id):
        """Lista hospitais por província"""
        HospitalService = ServiceFactory.get_hospital_service()
        hospitals = HospitalService.get_by_province(province_id)

        return {"success": True, "total": len(hospitals), "data": hospitals}, 200
