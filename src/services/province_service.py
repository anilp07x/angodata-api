"""
Serviço de lógica de negócio para Províncias.
Responsável por buscar e manipular dados de províncias.
"""

from src.models.province import PROVINCES


class ProvinceService:
    """Serviço para operações com províncias."""
    
    @staticmethod
    def get_all():
        """Retorna todas as províncias."""
        return PROVINCES
    
    @staticmethod
    def get_by_id(province_id):
        """
        Retorna uma província específica por ID.
        
        Args:
            province_id (int): ID da província
            
        Returns:
            dict ou None: Dados da província ou None se não encontrada
        """
        province_id = int(province_id)
        for province in PROVINCES:
            if province['id'] == province_id:
                return province
        return None
