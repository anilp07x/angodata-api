"""
Serviço de lógica de negócio para Hospitais.
Responsável por buscar e manipular dados de hospitais.
"""

from src.models.hospital import HOSPITALS
from src.utils.persistence import persist_data


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
    
    @staticmethod
    def get_by_municipality(municipality_id):
        """
        Retorna todos os hospitais de um município específico.
        
        Args:
            municipality_id (int): ID do município
            
        Returns:
            list: Lista de hospitais do município
        """
        municipality_id = int(municipality_id)
        return [h for h in HOSPITALS if h.get('municipio_id') == municipality_id]
    
    @staticmethod
    def create(data):
        """
        Cria um novo hospital.
        
        Args:
            data (dict): Dados do hospital
            
        Returns:
            dict ou None: Hospital criado ou None se validação falhar
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
        new_id = max([h['id'] for h in HOSPITALS]) + 1 if HOSPITALS else 1
        
        new_hospital = {
            'id': new_id,
            'nome': data['nome'],
            'tipo': data['tipo'],
            'categoria': data['categoria'],
            'provincia_id': data['provincia_id'],
            'provincia_nome': province['nome'],
            'municipio_id': data['municipio_id'],
            'municipio': municipality['nome'],
            'endereco': data['endereco']
        }
        
        HOSPITALS.append(new_hospital)
        return new_hospital
    
    @staticmethod
    @persist_data
    def update(hospital_id, data):
        """
        Atualiza um hospital existente.
        
        Args:
            hospital_id (int): ID do hospital
            data (dict): Dados para atualizar
            
        Returns:
            dict ou None: Hospital atualizado ou None se não encontrado/validação falhar
        """
        from src.services.province_service import ProvinceService
        from src.services.municipality_service import MunicipalityService
        
        hospital_id = int(hospital_id)
        for hospital in HOSPITALS:
            if hospital['id'] == hospital_id:
                # Atualizar campos simples
                if 'nome' in data:
                    hospital['nome'] = data['nome']
                if 'tipo' in data:
                    hospital['tipo'] = data['tipo']
                if 'categoria' in data:
                    hospital['categoria'] = data['categoria']
                if 'endereco' in data:
                    hospital['endereco'] = data['endereco']
                
                # Atualizar província/município
                if 'provincia_id' in data or 'municipio_id' in data:
                    provincia_id = data.get('provincia_id', hospital['provincia_id'])
                    municipio_id = data.get('municipio_id', hospital['municipio_id'])
                    
                    province = ProvinceService.get_by_id(provincia_id)
                    if not province:
                        return None
                    
                    municipality = MunicipalityService.get_by_id(municipio_id)
                    if not municipality:
                        return None
                    
                    if municipality['provincia_id'] != provincia_id:
                        return None
                    
                    hospital['provincia_id'] = provincia_id
                    hospital['provincia_nome'] = province['nome']
                    hospital['municipio_id'] = municipio_id
                    hospital['municipio'] = municipality['nome']
                
                return hospital
        return None
    
    @staticmethod
    @persist_data
    def delete(hospital_id):
        """
        Deleta um hospital.
        
        Args:
            hospital_id (int): ID do hospital
            
        Returns:
            bool: True se deletado, False se não encontrado
        """
        hospital_id = int(hospital_id)
        for i, hospital in enumerate(HOSPITALS):
            if hospital['id'] == hospital_id:
                HOSPITALS.pop(i)
                return True
        return False
