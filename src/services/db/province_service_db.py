"""
Province service using SQLAlchemy ORM.
Provides database-backed operations for provinces.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.database.base import get_db_session
from src.database.models import Municipality, Province
from src.utils.pagination import PaginationHelper, SearchHelper


class ProvinceServiceDB:
    """Service for managing provinces with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        Get all provinces from database.

        Returns:
            List[Dict]: List of all provinces with their data
        """
        try:
            with get_db_session() as session:
                provinces = session.query(Province).order_by(Province.nome).all()
                return [province.to_dict() for province in provinces]
        except SQLAlchemyError as e:
            print(f"Database error getting all provinces: {e}")
            return []

    @staticmethod
    def get_all_paginated(
        page: int = 1, per_page: int = 20, sort_by: str = "nome", order: str = "asc", search: str = None
    ) -> Dict[str, Any]:
        """
        Get paginated provinces with search and sort.

        Args:
            page: Page number (1-indexed)
            per_page: Items per page
            sort_by: Field to sort by
            order: 'asc' or 'desc'
            search: Search term for nome or capital

        Returns:
            Dict with paginated data and metadata
        """
        try:
            with get_db_session() as session:
                query = session.query(Province)

                # Aplicar busca
                if search:
                    query = SearchHelper.apply_text_search(query, Province, search, ["nome", "capital"])

                # Aplicar ordenação
                query = SearchHelper.apply_sorting(query, Province, sort_by, order)

                # Aplicar paginação
                return PaginationHelper.paginate_query(query, page, per_page)

        except SQLAlchemyError as e:
            print(f"Database error getting paginated provinces: {e}")
            return {
                "data": [],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_items": 0,
                    "total_pages": 0,
                    "has_next": False,
                    "has_prev": False,
                },
            }

    @staticmethod
    def get_by_id(province_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific province by ID.

        Args:
            province_id: The ID of the province to retrieve

        Returns:
            Dict or None: Province data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                province = session.query(Province).filter(Province.id == province_id).first()
                return province.to_dict() if province else None
        except SQLAlchemyError as e:
            print(f"Database error getting province {province_id}: {e}")
            return None

    @staticmethod
    def get_by_name(nome: str) -> Optional[Dict[str, Any]]:
        """
        Get a province by name (case-insensitive).

        Args:
            nome: Name of the province

        Returns:
            Dict or None: Province data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                province = session.query(Province).filter(Province.nome.ilike(nome)).first()
                return province.to_dict() if province else None
        except SQLAlchemyError as e:
            print(f"Database error getting province by name '{nome}': {e}")
            return None

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new province.

        Args:
            data: Province data (nome, capital, area_km2, populacao)

        Returns:
            Dict or None: Created province data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                province = Province(
                    nome=data["nome"],
                    capital=data.get("capital"),
                    area_km2=data.get("area_km2"),
                    populacao=data.get("populacao"),
                )
                session.add(province)
                session.flush()  # Get the ID before commit
                result = province.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error creating province: {e}")
            return None

    @staticmethod
    def update(province_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing province.

        Args:
            province_id: ID of the province to update
            data: Updated province data

        Returns:
            Dict or None: Updated province data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                province = session.query(Province).filter(Province.id == province_id).first()

                if not province:
                    return None

                # Update fields if provided
                if "nome" in data:
                    province.nome = data["nome"]
                if "capital" in data:
                    province.capital = data["capital"]
                if "area_km2" in data:
                    province.area_km2 = data["area_km2"]
                if "populacao" in data:
                    province.populacao = data["populacao"]

                session.flush()
                result = province.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error updating province {province_id}: {e}")
            return None

    @staticmethod
    def delete(province_id: int) -> bool:
        """
        Delete a province by ID.

        Args:
            province_id: ID of the province to delete

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            with get_db_session() as session:
                province = session.query(Province).filter(Province.id == province_id).first()

                if not province:
                    return False

                session.delete(province)
                return True
        except SQLAlchemyError as e:
            print(f"Database error deleting province {province_id}: {e}")
            return False

    @staticmethod
    def count() -> int:
        """
        Get total count of provinces.

        Returns:
            int: Total number of provinces
        """
        try:
            with get_db_session() as session:
                return session.query(Province).count()
        except SQLAlchemyError as e:
            print(f"Database error counting provinces: {e}")
            return 0

    @staticmethod
    def has_municipalities(province_id: int) -> int:
        """
        Check how many municipalities belong to a province.

        Args:
            province_id: ID of the province

        Returns:
            int: Number of municipalities in the province
        """
        try:
            with get_db_session() as session:
                return session.query(Municipality).filter(Municipality.provincia_id == province_id).count()
        except SQLAlchemyError as e:
            print(f"Database error checking municipalities for province {province_id}: {e}")
            return 0

    @staticmethod
    def bulk_create(provinces_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple provinces at once.

        Args:
            provinces_data: List of province data dictionaries

        Returns:
            Dict with created count and any errors
        """
        try:
            with get_db_session() as session:
                created = []
                errors = []

                for data in provinces_data:
                    try:
                        province = Province(
                            nome=data["nome"],
                            capital=data.get("capital"),
                            area_km2=data.get("area_km2"),
                            populacao=data.get("populacao"),
                        )
                        session.add(province)
                        session.flush()
                        created.append(province.to_dict())
                    except Exception as e:
                        errors.append({"data": data, "error": str(e)})

                return {"created": len(created), "failed": len(errors), "data": created, "errors": errors}

        except SQLAlchemyError as e:
            print(f"Database error in bulk create: {e}")
            return {"created": 0, "failed": len(provinces_data), "data": [], "errors": [{"error": str(e)}]}

    @staticmethod
    def bulk_update(updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update multiple provinces at once.

        Args:
            updates: List of dicts with 'id' and fields to update

        Returns:
            Dict with updated count and any errors
        """
        try:
            with get_db_session() as session:
                updated = []
                errors = []

                for update_data in updates:
                    try:
                        province_id = update_data.get("id")
                        if not province_id:
                            errors.append({"data": update_data, "error": "Missing id"})
                            continue

                        province = session.query(Province).filter(Province.id == province_id).first()

                        if not province:
                            errors.append({"id": province_id, "error": "Not found"})
                            continue

                        # Update fields
                        if "nome" in update_data:
                            province.nome = update_data["nome"]
                        if "capital" in update_data:
                            province.capital = update_data["capital"]
                        if "area_km2" in update_data:
                            province.area_km2 = update_data["area_km2"]
                        if "populacao" in update_data:
                            province.populacao = update_data["populacao"]

                        session.flush()
                        updated.append(province.to_dict())

                    except Exception as e:
                        errors.append({"data": update_data, "error": str(e)})

                return {"updated": len(updated), "failed": len(errors), "data": updated, "errors": errors}

        except SQLAlchemyError as e:
            print(f"Database error in bulk update: {e}")
            return {"updated": 0, "failed": len(updates), "data": [], "errors": [{"error": str(e)}]}

    @staticmethod
    def bulk_delete(province_ids: List[int]) -> Dict[str, Any]:
        """
        Delete multiple provinces at once.

        Args:
            province_ids: List of province IDs to delete

        Returns:
            Dict with deleted count and any errors
        """
        try:
            with get_db_session() as session:
                deleted = []
                errors = []

                for province_id in province_ids:
                    try:
                        province = session.query(Province).filter(Province.id == province_id).first()

                        if not province:
                            errors.append({"id": province_id, "error": "Not found"})
                            continue

                        session.delete(province)
                        deleted.append(province_id)

                    except Exception as e:
                        errors.append({"id": province_id, "error": str(e)})

                return {"deleted": len(deleted), "failed": len(errors), "ids": deleted, "errors": errors}

        except SQLAlchemyError as e:
            print(f"Database error in bulk delete: {e}")
            return {"deleted": 0, "failed": len(province_ids), "ids": [], "errors": [{"error": str(e)}]}
