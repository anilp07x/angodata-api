"""
Serviço de lógica de negócio para Municípios.
Responsável por buscar e manipular dados de municípios.
"""

from src.models.municipality import MUNICIPALITIES
from src.utils.persistence import persist_data


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
    
    @staticmethod
    @persist_data
    def create(data):
        """
        Cria um novo município.
        
        Args:
            data (dict): Dados do município (nome, provincia_id)
            
        Returns:
            dict: Município criado com ID gerado
        """
        from src.services.province_service import ProvinceService
        
        # Validar se província existe
        province = ProvinceService.get_by_id(data['provincia_id'])
        if not province:
            return None
        
        # Gerar novo ID
        new_id = max([m['id'] for m in MUNICIPALITIES]) + 1 if MUNICIPALITIES else 1
        
        new_municipality = {
            'id': new_id,
            'nome': data['nome'],
            'provincia_id': data['provincia_id'],
            'provincia_nome': province['nome']
        }
        
        MUNICIPALITIES.append(new_municipality)
        return new_municipality
    
    @staticmethod
    @persist_data
    def update(municipality_id, data):
        """
        Atualiza um município existente.
        
        Args:
            municipality_id (int): ID do município
            data (dict): Dados para atualizar
            
        Returns:
            dict ou None: Município atualizado ou None se não encontrado
        """
        from src.services.province_service import ProvinceService
        
        municipality_id = int(municipality_id)
        for municipality in MUNICIPALITIES:
            if municipality['id'] == municipality_id:
                # Atualizar campos fornecidos
                if 'nome' in data:
                    municipality['nome'] = data['nome']
                
                if 'provincia_id' in data:
                    # Validar se nova província existe
                    province = ProvinceService.get_by_id(data['provincia_id'])
                    if not province:
                        return None
                    municipality['provincia_id'] = data['provincia_id']
                    municipality['provincia_nome'] = province['nome']
                
                return municipality
        return None
    
    @staticmethod
    @persist_data
    def delete(municipality_id):
        """
        Deleta um município.
        
        Args:
            municipality_id (int): ID do município
            
        Returns:
            bool: True se deletado, False se não encontrado
        """
        municipality_id = int(municipality_id)
        for i, municipality in enumerate(MUNICIPALITIES):
            if municipality['id'] == municipality_id:
                MUNICIPALITIES.pop(i)
                return True
        return False
    
    @staticmethod
    def has_dependencies(municipality_id):
        """
        Verifica se o município tem dependências (escolas, mercados, hospitais).
        
        Args:
            municipality_id (int): ID do município
            
        Returns:
            dict: Contadores de dependências por tipo
        """
        from src.models.school import SCHOOLS
        from src.models.market import MARKETS
        from src.models.hospital import HOSPITALS
        
        schools = sum(1 for s in SCHOOLS if s.get('municipio_id') == municipality_id)
        markets = sum(1 for m in MARKETS if m.get('municipio_id') == municipality_id)
        hospitals = sum(1 for h in HOSPITALS if h.get('municipio_id') == municipality_id)
        
        return {
            'schools': schools,
            'markets': markets,
            'hospitals': hospitals,
            'total': schools + markets + hospitals
        }
