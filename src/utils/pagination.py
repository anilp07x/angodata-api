"""
Helpers para paginação e busca avançada.
"""

from typing import Any, Dict, List, Optional, Tuple

from flask import request
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Query


class PaginationHelper:
    """Helper para paginação de resultados."""

    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100

    @staticmethod
    def get_pagination_params() -> Tuple[int, int]:
        """
        Extrai parâmetros de paginação da query string.

        Returns:
            Tuple[int, int]: (page, per_page)
        """
        page = request.args.get("page", PaginationHelper.DEFAULT_PAGE, type=int)
        per_page = request.args.get("per_page", PaginationHelper.DEFAULT_PER_PAGE, type=int)

        # Validar limites
        page = max(1, page)
        per_page = min(max(1, per_page), PaginationHelper.MAX_PER_PAGE)

        return page, per_page

    @staticmethod
    def paginate_query(query: Query, page: int, per_page: int) -> Dict[str, Any]:
        """
        Aplica paginação em uma query SQLAlchemy.

        Args:
            query: Query SQLAlchemy
            page: Número da página (1-indexed)
            per_page: Itens por página

        Returns:
            Dict com dados paginados e metadados
        """
        # Contar total de resultados
        total = query.count()

        # Calcular offset
        offset = (page - 1) * per_page

        # Aplicar limit e offset
        items = query.limit(per_page).offset(offset).all()

        # Calcular total de páginas
        total_pages = (total + per_page - 1) // per_page if total > 0 else 0

        return {
            "data": [item.to_dict() for item in items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
                "next_page": page + 1 if page < total_pages else None,
                "prev_page": page - 1 if page > 1 else None,
            },
        }

    @staticmethod
    def paginate_list(items: List[Any], page: int, per_page: int) -> Dict[str, Any]:
        """
        Aplica paginação em uma lista Python (para modo JSON).

        Args:
            items: Lista de itens
            page: Número da página (1-indexed)
            per_page: Itens por página

        Returns:
            Dict com dados paginados e metadados
        """
        total = len(items)
        total_pages = (total + per_page - 1) // per_page if total > 0 else 0

        # Calcular offset
        offset = (page - 1) * per_page
        end = offset + per_page

        # Slice da lista
        paginated_items = items[offset:end]

        return {
            "data": paginated_items,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
                "next_page": page + 1 if page < total_pages else None,
                "prev_page": page - 1 if page > 1 else None,
            },
        }


class SearchHelper:
    """Helper para busca avançada e filtros."""

    @staticmethod
    def get_sort_params() -> Tuple[Optional[str], str]:
        """
        Extrai parâmetros de ordenação da query string.

        Returns:
            Tuple[str, str]: (sort_by, order) - order é 'asc' ou 'desc'
        """
        sort_by = request.args.get("sort_by", None, type=str)
        order = request.args.get("order", "asc", type=str).lower()

        # Validar order
        if order not in ["asc", "desc"]:
            order = "asc"

        return sort_by, order

    @staticmethod
    def apply_sorting(query: Query, model: Any, sort_by: Optional[str], order: str) -> Query:
        """
        Aplica ordenação em uma query SQLAlchemy.

        Args:
            query: Query SQLAlchemy
            model: Model class
            sort_by: Nome do campo para ordenar
            order: 'asc' ou 'desc'

        Returns:
            Query com ordenação aplicada
        """
        if not sort_by:
            return query

        # Verificar se o campo existe no model
        if not hasattr(model, sort_by):
            return query

        # Aplicar ordenação
        field = getattr(model, sort_by)
        if order == "desc":
            return query.order_by(field.desc())
        else:
            return query.order_by(field.asc())

    @staticmethod
    def get_search_query() -> Optional[str]:
        """
        Extrai termo de busca da query string.

        Returns:
            str: Termo de busca ou None
        """
        return request.args.get("search", None, type=str)

    @staticmethod
    def apply_text_search(query: Query, model: Any, search_term: str, search_fields: List[str]) -> Query:
        """
        Aplica busca de texto em múltiplos campos.

        Args:
            query: Query SQLAlchemy
            model: Model class
            search_term: Termo para buscar
            search_fields: Lista de campos onde buscar

        Returns:
            Query com filtro de busca aplicado
        """
        if not search_term:
            return query

        # Criar condições OR para cada campo
        conditions = []
        search_pattern = f"%{search_term}%"

        for field_name in search_fields:
            if hasattr(model, field_name):
                field = getattr(model, field_name)
                # Usar ilike para case-insensitive search
                conditions.append(field.ilike(search_pattern))

        if conditions:
            return query.filter(or_(*conditions))

        return query

    @staticmethod
    def apply_filters(query: Query, model: Any, filters: Dict[str, Any]) -> Query:
        """
        Aplica múltiplos filtros em uma query.

        Args:
            query: Query SQLAlchemy
            model: Model class
            filters: Dicionário de {campo: valor}

        Returns:
            Query com filtros aplicados
        """
        for field_name, value in filters.items():
            if hasattr(model, field_name) and value is not None:
                field = getattr(model, field_name)
                query = query.filter(field == value)

        return query

    @staticmethod
    def apply_range_filter(query: Query, model: Any, field_name: str, min_value: Any = None, max_value: Any = None) -> Query:
        """
        Aplica filtro de range (min/max) em um campo numérico.

        Args:
            query: Query SQLAlchemy
            model: Model class
            field_name: Nome do campo
            min_value: Valor mínimo (inclusive)
            max_value: Valor máximo (inclusive)

        Returns:
            Query com filtro de range aplicado
        """
        if not hasattr(model, field_name):
            return query

        field = getattr(model, field_name)

        if min_value is not None:
            query = query.filter(field >= min_value)

        if max_value is not None:
            query = query.filter(field <= max_value)

        return query
