"""
Serviço de lógica de negócio para Mercados.
Responsável por buscar e manipular dados de mercados.
"""

from src.models.market import MARKETS
from src.utils.persistence import persist_data


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
    
    @staticmethod
    def get_by_municipality(municipality_id):
        """
        Retorna todos os mercados de um município específico.
        
        Args:
            municipality_id (int): ID do município
            
        Returns:
            list: Lista de mercados do município
        """
        municipality_id = int(municipality_id)
        return [m for m in MARKETS if m.get('municipio_id') == municipality_id]
    
    @staticmethod
    def create(data):
        """
        Cria um novo mercado.
        
        Args:
            data (dict): Dados do mercado
            
        Returns:
            dict ou None: Mercado criado ou None se validação falhar
        """
        from src.services.province_service import ProvinceService
        from src.services.municipality_service import MunicipalityService
        
        # Validar província
        province = ProvinceService.get_by_id(data['provincia_id'])
        if not province:
            return None
        
        # Validar município
        municipality = MunicipalityService.get_by_id(data['municipio_id'])
        if not municipality:
            return None
        
        # Validar se município pertence à província
        if municipality['provincia_id'] != data['provincia_id']:
            return None
        
        # Gerar novo ID
        new_id = max([m['id'] for m in MARKETS]) + 1 if MARKETS else 1
        
        new_market = {
            'id': new_id,
            'nome': data['nome'],
            'tipo': data['tipo'],
            'provincia_id': data['provincia_id'],
            'provincia_nome': province['nome'],
            'municipio_id': data['municipio_id'],
            'municipio': municipality['nome'],
            'especialidade': data['especialidade']
        }
        
        MARKETS.append(new_market)
        return new_market
    
    @staticmethod
    @persist_data
    def update(market_id, data):
        """
        Atualiza um mercado existente.
        
        Args:
            market_id (int): ID do mercado
            data (dict): Dados para atualizar
            
        Returns:
            dict ou None: Mercado atualizado ou None se não encontrado/validação falhar
        """
        from src.services.province_service import ProvinceService
        from src.services.municipality_service import MunicipalityService
        
        market_id = int(market_id)
        for market in MARKETS:
            if market['id'] == market_id:
                # Atualizar campos simples
                if 'nome' in data:
                    market['nome'] = data['nome']
                if 'tipo' in data:
                    market['tipo'] = data['tipo']
                if 'especialidade' in data:
                    market['especialidade'] = data['especialidade']
                
                # Atualizar província/município
                if 'provincia_id' in data or 'municipio_id' in data:
                    provincia_id = data.get('provincia_id', market['provincia_id'])
                    municipio_id = data.get('municipio_id', market['municipio_id'])
                    
                    province = ProvinceService.get_by_id(provincia_id)
                    if not province:
                        return None
                    
                    municipality = MunicipalityService.get_by_id(municipio_id)
                    if not municipality:
                        return None
                    
                    if municipality['provincia_id'] != provincia_id:
                        return None
                    
                    market['provincia_id'] = provincia_id
                    market['provincia_nome'] = province['nome']
                    market['municipio_id'] = municipio_id
                    market['municipio'] = municipality['nome']
                
                return market
        return None
    
    @staticmethod
    @persist_data
    def delete(market_id):
        """
        Deleta um mercado.
        
        Args:
            market_id (int): ID do mercado
            
        Returns:
            bool: True se deletado, False se não encontrado
        """
        market_id = int(market_id)
        for i, market in enumerate(MARKETS):
            if market['id'] == market_id:
                MARKETS.pop(i)
                return True
        return False
