"""
Serviço de lógica de negócio para Hospitais.
Responsável por buscar e manipular dados de hospitais.
"""

from src.models.hospital import HOSPITALS


class HospitalService:
    """Serviço para operações com hospitais."""
    
    @staticmethod
    def get_all():
        """Retorna todos os hospitais."""
        return HOSPITALS
    
    @staticmethod
    def get_by_id(hospital_id):
        """
        Retorna um hospital específico por ID.
        
        Args:
            hospital_id (int): ID do hospital
            
        Returns:
            dict ou None: Dados do hospital ou None se não encontrado
        """
        hospital_id = int(hospital_id)
        for hospital in HOSPITALS:
            if hospital['id'] == hospital_id:
                return hospital
        return None
    
    @staticmethod
    def get_by_province(province_id):
        """
        Retorna todos os hospitais de uma província específica.
        
        Args:
            province_id (int): ID da província
            
        Returns:
            list: Lista de hospitais da província
        """
        province_id = int(province_id)
        return [h for h in HOSPITALS if h['provincia_id'] == province_id]
