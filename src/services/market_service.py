"""
Serviço de lógica de negócio para Mercados.
Responsável por buscar e manipular dados de mercados.
"""

from src.models.market import MARKETS


class MarketService:
    """Serviço para operações com mercados."""
    
    @staticmethod
    def get_all():
        """Retorna todos os mercados."""
        return MARKETS
    
    @staticmethod
    def get_by_id(market_id):
        """
        Retorna um mercado específico por ID.
        
        Args:
            market_id (int): ID do mercado
            
        Returns:
            dict ou None: Dados do mercado ou None se não encontrado
        """
        market_id = int(market_id)
        for market in MARKETS:
            if market['id'] == market_id:
                return market
        return None
    
    @staticmethod
    def get_by_province(province_id):
        """
        Retorna todos os mercados de uma província específica.
        
        Args:
            province_id (int): ID da província
            
        Returns:
            list: Lista de mercados da província
        """
        province_id = int(province_id)
        return [m for m in MARKETS if m['provincia_id'] == province_id]
