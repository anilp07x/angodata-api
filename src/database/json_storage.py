"""
Sistema de persistência JSON para dados in-memory.
Salva e carrega dados automaticamente de arquivos JSON.
"""

import json
import os
from pathlib import Path


class JSONStorage:
    """Gerenciador de persistência JSON"""
    
    # Diretório onde os dados serão salvos
    DATA_DIR = Path(__file__).parent.parent.parent / 'data'
    
    @classmethod
    def ensure_data_dir(cls):
        """Garante que o diretório de dados existe"""
        cls.DATA_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def save(cls, filename, data):
        """
        Salva dados em arquivo JSON.
        
        Args:
            filename (str): Nome do arquivo (ex: 'provinces.json')
            data (list): Lista de dados para salvar
        """
        cls.ensure_data_dir()
        filepath = cls.DATA_DIR / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar {filename}: {e}")
            return False
    
    @classmethod
    def load(cls, filename, default=None):
        """
        Carrega dados de arquivo JSON.
        
        Args:
            filename (str): Nome do arquivo (ex: 'provinces.json')
            default: Valor padrão se arquivo não existir
            
        Returns:
            list: Dados carregados ou default
        """
        filepath = cls.DATA_DIR / filename
        
        if not filepath.exists():
            return default if default is not None else []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar {filename}: {e}")
            return default if default is not None else []
    
    @classmethod
    def save_all_entities(cls):
        """
        Salva todas as entidades em seus respectivos arquivos.
        Deve ser chamado após operações de CREATE/UPDATE/DELETE.
        """
        from src.models.province import PROVINCES
        from src.models.municipality import MUNICIPALITIES
        from src.models.school import SCHOOLS
        from src.models.market import MARKETS
        from src.models.hospital import HOSPITALS
        
        cls.save('provinces.json', PROVINCES)
        cls.save('municipalities.json', MUNICIPALITIES)
        cls.save('schools.json', SCHOOLS)
        cls.save('markets.json', MARKETS)
        cls.save('hospitals.json', HOSPITALS)
    
    @classmethod
    def load_all_entities(cls):
        """
        Carrega todas as entidades de seus arquivos.
        Deve ser chamado na inicialização da aplicação.
        
        Returns:
            dict: Dicionário com todas as entidades carregadas
        """
        return {
            'provinces': cls.load('provinces.json'),
            'municipalities': cls.load('municipalities.json'),
            'schools': cls.load('schools.json'),
            'markets': cls.load('markets.json'),
            'hospitals': cls.load('hospitals.json')
        }
