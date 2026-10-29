"""
Hospital service using SQLAlchemy ORM.
Provides database-backed operations for hospitals.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import joinedload

from src.database.base import get_db_session
from src.database.models import Hospital
from src.services.db.common import resolve_location


class HospitalServiceDB:
    """Service for managing hospitals with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all hospitals from database."""
        with get_db_session() as session:
            hospitals = (
                session.query(Hospital)
                .options(joinedload(Hospital.province), joinedload(Hospital.municipality))
                .order_by(Hospital.nome)
                .all()
            )
            return [hospital.to_dict() for hospital in hospitals]

    @staticmethod
    def get_by_id(hospital_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific hospital by ID."""
        with get_db_session() as session:
            hospital = (
                session.query(Hospital)
                .options(joinedload(Hospital.province), joinedload(Hospital.municipality))
                .filter(Hospital.id == hospital_id)
                .first()
            )
            return hospital.to_dict() if hospital else None

    @staticmethod
    def get_by_province(province_id: int) -> List[Dict[str, Any]]:
        """Get all hospitals for a specific province."""
        with get_db_session() as session:
            hospitals = (
                session.query(Hospital)
                .options(joinedload(Hospital.province), joinedload(Hospital.municipality))
                .filter(Hospital.provincia_id == province_id)
                .order_by(Hospital.nome)
                .all()
            )
            return [hospital.to_dict() for hospital in hospitals]

    @staticmethod
    def get_by_municipality(municipio_id: int) -> List[Dict[str, Any]]:
        """Get all hospitals for a specific municipality (by municipality ID)."""
        with get_db_session() as session:
            hospitals = (
                session.query(Hospital)
                .options(joinedload(Hospital.province), joinedload(Hospital.municipality))
                .filter(Hospital.municipio_id == int(municipio_id))
                .order_by(Hospital.nome)
                .all()
            )
            return [hospital.to_dict() for hospital in hospitals]

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new hospital (validates province/municipality relationship)."""
        with get_db_session() as session:
            location = resolve_location(
                session, data["provincia_id"], data.get("municipio_id")
            )
            if not location:
                return None

            provincia_nome, municipio_id, municipio_nome = location
            hospital = Hospital(
                nome=data["nome"],
                tipo=data.get("tipo"),
                categoria=data.get("categoria"),
                provincia_id=data["provincia_id"],
                municipio_id=municipio_id,
                municipio=municipio_nome,
                endereco=data.get("endereco"),
                especialidades=data.get("especialidades"),
            )
            session.add(hospital)
            session.flush()
            result = hospital.to_dict()
            result["provincia_nome"] = provincia_nome
            return result

    @staticmethod
    def update(hospital_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing hospital (validates province/municipality relationship)."""
        with get_db_session() as session:
            hospital = (
                session.query(Hospital)
                .options(joinedload(Hospital.province), joinedload(Hospital.municipality))
                .filter(Hospital.id == hospital_id)
                .first()
            )

            if not hospital:
                return None

            # Atualizar província/município (validar antes de mutar o modelo)
            location = None
            if "provincia_id" in data or "municipio_id" in data:
                provincia_id = data.get("provincia_id", hospital.provincia_id)
                municipio_id = data.get("municipio_id", hospital.municipio_id)

                location = resolve_location(session, provincia_id, municipio_id)
                if not location:
                    return None

                provincia_nome, municipio_id, municipio_nome = location
                hospital.provincia_id = provincia_id
                hospital.municipio_id = municipio_id
                hospital.municipio = municipio_nome

            if "nome" in data:
                hospital.nome = data["nome"]
            if "tipo" in data:
                hospital.tipo = data["tipo"]
            if "categoria" in data:
                hospital.categoria = data["categoria"]
            if "endereco" in data:
                hospital.endereco = data["endereco"]
            if "especialidades" in data:
                hospital.especialidades = data["especialidades"]

            session.flush()
            result = hospital.to_dict()
            if location is not None:
                result["provincia_nome"] = provincia_nome
            return result

    @staticmethod
    def delete(hospital_id: int) -> bool:
        """Delete a hospital by ID."""
        with get_db_session() as session:
            hospital = session.query(Hospital).filter(Hospital.id == hospital_id).first()

            if not hospital:
                return False

            session.delete(hospital)
            return True

    @staticmethod
    def count() -> int:
        """Get total count of hospitals."""
        with get_db_session() as session:
            return session.query(Hospital).count()
