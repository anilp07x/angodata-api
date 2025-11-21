"""
Serviço de lógica de negócio para Escolas.
Responsável por buscar e manipular dados de escolas.
"""

from src.models.school import SCHOOLS


class SchoolService:
    """Serviço para operações com escolas."""
    
    @staticmethod
    def get_all():
        """Retorna todas as escolas."""
        return SCHOOLS
    
    @staticmethod
    def get_by_id(school_id):
        """
        Retorna uma escola específica por ID.
        
        Args:
            school_id (int): ID da escola
            
        Returns:
            dict ou None: Dados da escola ou None se não encontrada
        """
        school_id = int(school_id)
        for school in SCHOOLS:
            if school['id'] == school_id:
                return school
        return None
    
    @staticmethod
    def get_by_province(province_id):
        """
        Retorna todas as escolas de uma província específica.
        
        Args:
            province_id (int): ID da província
            
        Returns:
            list: Lista de escolas da província
        """
        province_id = int(province_id)
        return [s for s in SCHOOLS if s['provincia_id'] == province_id]
