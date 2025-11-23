"""
School service using SQLAlchemy ORM.
Provides database-backed operations for schools.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError

from src.database.base import get_db_session
from src.database.models import School


class SchoolServiceDB:
    """Service for managing schools with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        Get all schools from database.
        
        Returns:
            List[Dict]: List of all schools with their data
        """
        try:
            with get_db_session() as session:
                schools = session.query(School).order_by(School.nome).all()
                return [school.to_dict() for school in schools]
        except SQLAlchemyError as e:
            print(f"Database error getting all schools: {e}")
            return []

    @staticmethod
    def get_by_id(school_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific school by ID.
        
        Args:
            school_id: The ID of the school to retrieve
            
        Returns:
            Dict or None: School data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                school = session.query(School).filter(
                    School.id == school_id
                ).first()
                return school.to_dict() if school else None
        except SQLAlchemyError as e:
            print(f"Database error getting school {school_id}: {e}")
            return None

    @staticmethod
    def get_by_province(province_id: int) -> List[Dict[str, Any]]:
        """
        Get all schools for a specific province.
        
        Args:
            province_id: ID of the province
            
        Returns:
            List[Dict]: List of schools in the province
        """
        try:
            with get_db_session() as session:
                schools = session.query(School).filter(
                    School.provincia_id == province_id
                ).order_by(School.nome).all()
                return [school.to_dict() for school in schools]
        except SQLAlchemyError as e:
            print(f"Database error getting schools for province {province_id}: {e}")
            return []

    @staticmethod
    def get_by_municipality(municipio_nome: str) -> List[Dict[str, Any]]:
        """
        Get all schools for a specific municipality.
        
        Args:
            municipio_nome: Name of the municipality
            
        Returns:
            List[Dict]: List of schools in the municipality
        """
        try:
            with get_db_session() as session:
                schools = session.query(School).filter(
                    School.municipio == municipio_nome
                ).order_by(School.nome).all()
                return [school.to_dict() for school in schools]
        except SQLAlchemyError as e:
            print(f"Database error getting schools for municipality '{municipio_nome}': {e}")
            return []

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new school.
        
        Args:
            data: School data (nome, provincia_id, municipio, tipo, nivel)
            
        Returns:
            Dict or None: Created school data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                school = School(
                    nome=data['nome'],
                    provincia_id=data['provincia_id'],
                    municipio=data.get('municipio'),
                    tipo=data.get('tipo'),
                    nivel=data.get('nivel')
                )
                session.add(school)
                session.flush()
                result = school.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error creating school: {e}")
            return None

    @staticmethod
    def update(school_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing school.
        
        Args:
            school_id: ID of the school to update
            data: Updated school data
            
        Returns:
            Dict or None: Updated school data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                school = session.query(School).filter(
                    School.id == school_id
                ).first()
                
                if not school:
                    return None
                
                # Update fields if provided
                if 'nome' in data:
                    school.nome = data['nome']
                if 'provincia_id' in data:
                    school.provincia_id = data['provincia_id']
                if 'municipio' in data:
                    school.municipio = data['municipio']
                if 'tipo' in data:
                    school.tipo = data['tipo']
                if 'nivel' in data:
                    school.nivel = data['nivel']
                
                session.flush()
                result = school.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error updating school {school_id}: {e}")
            return None

    @staticmethod
    def delete(school_id: int) -> bool:
        """
        Delete a school by ID.
        
        Args:
            school_id: ID of the school to delete
            
        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            with get_db_session() as session:
                school = session.query(School).filter(
                    School.id == school_id
                ).first()
                
                if not school:
                    return False
                
                session.delete(school)
                return True
        except SQLAlchemyError as e:
            print(f"Database error deleting school {school_id}: {e}")
            return False

    @staticmethod
    def count() -> int:
        """
        Get total count of schools.
        
        Returns:
            int: Total number of schools
        """
        try:
            with get_db_session() as session:
                return session.query(School).count()
        except SQLAlchemyError as e:
            print(f"Database error counting schools: {e}")
            return 0
