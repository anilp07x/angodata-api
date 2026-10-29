"""
School service using SQLAlchemy ORM.
Provides database-backed operations for schools.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import joinedload

from src.database.base import get_db_session
from src.database.models import School
from src.services.db.common import resolve_location


class SchoolServiceDB:
    """Service for managing schools with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all schools from database."""
        with get_db_session() as session:
            schools = (
                session.query(School)
                .options(joinedload(School.province), joinedload(School.municipality))
                .order_by(School.nome)
                .all()
            )
            return [school.to_dict() for school in schools]

    @staticmethod
    def get_by_id(school_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific school by ID."""
        with get_db_session() as session:
            school = (
                session.query(School)
                .options(joinedload(School.province), joinedload(School.municipality))
                .filter(School.id == school_id)
                .first()
            )
            return school.to_dict() if school else None

    @staticmethod
    def get_by_province(province_id: int) -> List[Dict[str, Any]]:
        """Get all schools for a specific province."""
        with get_db_session() as session:
            schools = (
                session.query(School)
                .options(joinedload(School.province), joinedload(School.municipality))
                .filter(School.provincia_id == province_id)
                .order_by(School.nome)
                .all()
            )
            return [school.to_dict() for school in schools]

    @staticmethod
    def get_by_municipality(municipio_id: int) -> List[Dict[str, Any]]:
        """Get all schools for a specific municipality (by municipality ID)."""
        with get_db_session() as session:
            schools = (
                session.query(School)
                .options(joinedload(School.province), joinedload(School.municipality))
                .filter(School.municipio_id == int(municipio_id))
                .order_by(School.nome)
                .all()
            )
            return [school.to_dict() for school in schools]

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new school (validates province/municipality relationship)."""
        with get_db_session() as session:
            location = resolve_location(
                session, data["provincia_id"], data.get("municipio_id")
            )
            if not location:
                return None

            provincia_nome, municipio_id, municipio_nome = location
            school = School(
                nome=data["nome"],
                tipo=data.get("tipo"),
                provincia_id=data["provincia_id"],
                municipio_id=municipio_id,
                municipio=municipio_nome,
                nivel=data.get("nivel"),
                endereco=data.get("endereco"),
            )
            session.add(school)
            session.flush()
            result = school.to_dict()  # attached: lazy relationships available
            result["provincia_nome"] = provincia_nome
            return result

    @staticmethod
    def update(school_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing school (validates province/municipality relationship)."""
        with get_db_session() as session:
            school = (
                session.query(School)
                .options(joinedload(School.province), joinedload(School.municipality))
                .filter(School.id == school_id)
                .first()
            )

            if not school:
                return None

            # Atualizar província/município (validar antes de mutar o modelo)
            location = None
            if "provincia_id" in data or "municipio_id" in data:
                provincia_id = data.get("provincia_id", school.provincia_id)
                municipio_id = data.get("municipio_id", school.municipio_id)

                location = resolve_location(session, provincia_id, municipio_id)
                if not location:
                    return None

                provincia_nome, municipio_id, municipio_nome = location
                school.provincia_id = provincia_id
                school.municipio_id = municipio_id
                school.municipio = municipio_nome

            if "nome" in data:
                school.nome = data["nome"]
            if "tipo" in data:
                school.tipo = data["tipo"]
            if "nivel" in data:
                school.nivel = data["nivel"]
            if "endereco" in data:
                school.endereco = data["endereco"]

            session.flush()
            result = school.to_dict()
            if "provincia_id" in data or "municipio_id" in data:
                result["provincia_nome"] = provincia_nome
            return result

    @staticmethod
    def delete(school_id: int) -> bool:
        """Delete a school by ID."""
        with get_db_session() as session:
            school = session.query(School).filter(School.id == school_id).first()

            if not school:
                return False

            session.delete(school)
            return True

    @staticmethod
    def count() -> int:
        """Get total count of schools."""
        with get_db_session() as session:
            return session.query(School).count()
