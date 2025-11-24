"""
Namespaces Swagger para escolas.
"""

from flask_restx import Namespace, fields

schools_ns = Namespace("schools", description="Operações com escolas de Angola")

school_model = schools_ns.model(
    "School",
    {
        "id": fields.Integer(readonly=True, description="ID único da escola"),
        "nome": fields.String(required=True, description="Nome da escola"),
        "provincia_id": fields.Integer(required=True, description="ID da província"),
        "provincia_nome": fields.String(readonly=True, description="Nome da província"),
        "tipo": fields.String(description="Tipo de escola", example="Primária"),
        "localizacao": fields.String(description="Localização da escola"),
    },
)

school_input = schools_ns.model(
    "SchoolInput",
    {
        "nome": fields.String(required=True, description="Nome da escola"),
        "provincia_id": fields.Integer(required=True, description="ID da província"),
        "tipo": fields.String(description="Tipo de escola"),
        "localizacao": fields.String(description="Localização"),
    },
)

pagination_metadata = schools_ns.model(
    "PaginationMetadata",
    {
        "page": fields.Integer(description="Página atual"),
        "per_page": fields.Integer(description="Itens por página"),
        "total_items": fields.Integer(description="Total de itens"),
        "total_pages": fields.Integer(description="Total de páginas"),
        "has_next": fields.Boolean(description="Tem próxima página"),
        "has_prev": fields.Boolean(description="Tem página anterior"),
    },
)

school_list_response = schools_ns.model(
    "SchoolListResponse",
    {
        "success": fields.Boolean(description="Status da operação"),
        "total": fields.Integer(description="Total de registros"),
        "data": fields.List(fields.Nested(school_model)),
        "pagination": fields.Nested(pagination_metadata, skip_none=True),
    },
)

school_response = schools_ns.model(
    "SchoolResponse", {"success": fields.Boolean(description="Status da operação"), "data": fields.Nested(school_model)}
)

error_response = schools_ns.model(
    "ErrorResponse",
    {
        "success": fields.Boolean(description="Status da operação", default=False),
        "message": fields.String(description="Mensagem de erro"),
    },
)
