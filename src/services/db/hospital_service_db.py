"""
Hospital service using SQLAlchemy ORM.
Provides database-backed operations for hospitals.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.exc import SQLAlchemyError

from src.database.base import get_db_session
from src.database.models import Hospital


class HospitalServiceDB:
    """Service for managing hospitals with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        Get all hospitals from database.

        Returns:
            List[Dict]: List of all hospitals with their data
        """
        try:
            with get_db_session() as session:
                hospitals = session.query(Hospital).order_by(Hospital.nome).all()
                return [hospital.to_dict() for hospital in hospitals]
        except SQLAlchemyError as e:
            print(f"Database error getting all hospitals: {e}")
            return []

    @staticmethod
    def get_by_id(hospital_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific hospital by ID.

        Args:
            hospital_id: The ID of the hospital to retrieve

        Returns:
            Dict or None: Hospital data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                hospital = session.query(Hospital).filter(Hospital.id == hospital_id).first()
                return hospital.to_dict() if hospital else None
        except SQLAlchemyError as e:
            print(f"Database error getting hospital {hospital_id}: {e}")
            return None

    @staticmethod
    def get_by_province(province_id: int) -> List[Dict[str, Any]]:
        """
        Get all hospitals for a specific province.

        Args:
            province_id: ID of the province

        Returns:
            List[Dict]: List of hospitals in the province
        """
        try:
            with get_db_session() as session:
                hospitals = session.query(Hospital).filter(Hospital.provincia_id == province_id).order_by(Hospital.nome).all()
                return [hospital.to_dict() for hospital in hospitals]
        except SQLAlchemyError as e:
            print(f"Database error getting hospitals for province {province_id}: {e}")
            return []

    @staticmethod
    def get_by_municipality(municipio_nome: str) -> List[Dict[str, Any]]:
        """
        Get all hospitals for a specific municipality.

        Args:
            municipio_nome: Name of the municipality

        Returns:
            List[Dict]: List of hospitals in the municipality
        """
        try:
            with get_db_session() as session:
                hospitals = session.query(Hospital).filter(Hospital.municipio == municipio_nome).order_by(Hospital.nome).all()
                return [hospital.to_dict() for hospital in hospitals]
        except SQLAlchemyError as e:
            print(f"Database error getting hospitals for municipality '{municipio_nome}': {e}")
            return []

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new hospital.

        Args:
            data: Hospital data (nome, provincia_id, municipio, tipo, endereco, especialidades)

        Returns:
            Dict or None: Created hospital data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                hospital = Hospital(
                    nome=data["nome"],
                    provincia_id=data["provincia_id"],
                    municipio=data.get("municipio"),
                    tipo=data.get("tipo"),
                    endereco=data.get("endereco"),
                    especialidades=data.get("especialidades"),
                )
                session.add(hospital)
                session.flush()
                result = hospital.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error creating hospital: {e}")
            return None

    @staticmethod
    def update(hospital_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing hospital.

        Args:
            hospital_id: ID of the hospital to update
            data: Updated hospital data

        Returns:
            Dict or None: Updated hospital data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                hospital = session.query(Hospital).filter(Hospital.id == hospital_id).first()

                if not hospital:
                    return None

                # Update fields if provided
                if "nome" in data:
                    hospital.nome = data["nome"]
                if "provincia_id" in data:
                    hospital.provincia_id = data["provincia_id"]
                if "municipio" in data:
                    hospital.municipio = data["municipio"]
                if "tipo" in data:
                    hospital.tipo = data["tipo"]
                if "endereco" in data:
                    hospital.endereco = data["endereco"]
                if "especialidades" in data:
                    hospital.especialidades = data["especialidades"]

                session.flush()
                result = hospital.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error updating hospital {hospital_id}: {e}")
            return None

    @staticmethod
    def delete(hospital_id: int) -> bool:
        """
        Delete a hospital by ID.

        Args:
            hospital_id: ID of the hospital to delete

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            with get_db_session() as session:
                hospital = session.query(Hospital).filter(Hospital.id == hospital_id).first()

                if not hospital:
                    return False

                session.delete(hospital)
                return True
        except SQLAlchemyError as e:
            print(f"Database error deleting hospital {hospital_id}: {e}")
            return False

    @staticmethod
    def count() -> int:
        """
        Get total count of hospitals.

        Returns:
            int: Total number of hospitals
        """
        try:
            with get_db_session() as session:
                return session.query(Hospital).count()
        except SQLAlchemyError as e:
            print(f"Database error counting hospitals: {e}")
            return 0
