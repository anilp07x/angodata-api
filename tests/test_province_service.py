"""
Testes unitários para ProvinceService.
"""

import pytest
from src.services.province_service import ProvinceService


class TestProvinceService:
    """Testes para o serviço de províncias."""
    
    def test_get_all_provinces(self):
        """Deve retornar lista de províncias."""
        provinces = ProvinceService.get_all()
        
        assert isinstance(provinces, list)
        assert len(provinces) > 0
        assert all('id' in p and 'nome' in p for p in provinces)
    
    def test_get_province_by_id(self):
        """Deve retornar província por ID."""
        province = ProvinceService.get_by_id(1)
        
        assert province is not None
        assert province['id'] == 1
        assert 'nome' in province
        assert 'capital' in province
    
    def test_create_and_delete_province(self):
        """Deve criar e deletar província."""
        # Contar antes
        count_before = len(ProvinceService.get_all())
        
        # Criar
        new_province = ProvinceService.create({
            'nome': 'Província Teste',
            'capital': 'Capital Teste',
            'area_km2': 10000,
            'populacao': 500000
        })
        
        assert new_province is not None
        assert new_province['nome'] == 'Província Teste'
        
        # Verificar que foi adicionada
        count_after = len(ProvinceService.get_all())
        assert count_after == count_before + 1
        
        # Cleanup - deletar
        if new_province:
            result = ProvinceService.delete(new_province['id'])
            assert result is True
            
            # Verificar que foi removida
            count_final = len(ProvinceService.get_all())
            assert count_final == count_before
