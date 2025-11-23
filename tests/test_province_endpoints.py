"""
Testes de integração para endpoints de províncias.
"""

import pytest
import json


class TestProvinceEndpoints:
    """Testes para os endpoints de províncias."""
    
    def test_get_province_by_id(self, client):
        """Deve retornar província por ID."""
        response = client.get('/provinces/1')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['id'] == 1
        assert 'nome' in data['data']
    
    def test_get_province_not_found(self, client):
        """Deve retornar 404 para província inexistente."""
        response = client.get('/provinces/9999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False
    
    def test_create_province_without_auth(self, client):
        """Deve retornar 401 sem autenticação."""
        response = client.post('/provinces',
            data=json.dumps({
                'nome': 'Test Province',
                'capital': 'Test Capital'
            }),
            content_type='application/json')
        
        assert response.status_code == 401
