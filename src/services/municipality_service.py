"""
Serviço de lógica de negócio para Municípios.
Responsável por buscar e manipular dados de municípios.
"""

from src.models.municipality import MUNICIPALITIES


class MunicipalityService:
    """Serviço para operações com municípios."""
    
    @staticmethod
    def get_all():
        """Retorna todos os municípios."""
        return MUNICIPALITIES
    
    @staticmethod
    def get_by_id(municipality_id):
        """
        Retorna um município específico por ID.
        
        Args:
            municipality_id (int): ID do município
            
        Returns:
            dict ou None: Dados do município ou None se não encontrado
        """
        municipality_id = int(municipality_id)
        for municipality in MUNICIPALITIES:
            if municipality['id'] == municipality_id:
                return municipality
        return None
    
    @staticmethod
    def get_by_province(province_id):
        """
        Retorna todos os municípios de uma província específica.
        
        Args:
            province_id (int): ID da província
            
        Returns:
            list: Lista de municípios da província
        """
        province_id = int(province_id)
        return [m for m in MUNICIPALITIES if m['provincia_id'] == province_id]
