"""
Serviço de lógica de negócio para Províncias.
Responsável por buscar e manipular dados de províncias.
"""

from src.models.province import PROVINCES
from src.utils.persistence import persist_data


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
            if province["id"] == province_id:
                return province
        return None

    @staticmethod
    @persist_data
    def create(data):
        """
        Cria uma nova província.

        Args:
            data (dict): Dados da província (nome, capital, area_km2, populacao)

        Returns:
            dict: Província criada com ID gerado
        """
        # Gerar novo ID (max + 1)
        new_id = max([p["id"] for p in PROVINCES]) + 1 if PROVINCES else 1

        new_province = {
            "id": new_id,
            "nome": data["nome"],
            "capital": data["capital"],
            "area_km2": data["area_km2"],
            "populacao": data["populacao"],
        }

        PROVINCES.append(new_province)
        return new_province

    @staticmethod
    @persist_data
    def update(province_id, data):
        """
        Atualiza uma província existente.

        Args:
            province_id (int): ID da província
            data (dict): Dados para atualizar

        Returns:
            dict ou None: Província atualizada ou None se não encontrada
        """
        province_id = int(province_id)
        for province in PROVINCES:
            if province["id"] == province_id:
                # Atualizar apenas campos fornecidos
                if "nome" in data:
                    province["nome"] = data["nome"]
                if "capital" in data:
                    province["capital"] = data["capital"]
                if "area_km2" in data:
                    province["area_km2"] = data["area_km2"]
                if "populacao" in data:
                    province["populacao"] = data["populacao"]
                return province
        return None

    @staticmethod
    @persist_data
    def delete(province_id):
        """
        Deleta uma província.

        Args:
            province_id (int): ID da província

        Returns:
            bool: True se deletado, False se não encontrado
        """
        province_id = int(province_id)
        for i, province in enumerate(PROVINCES):
            if province["id"] == province_id:
                PROVINCES.pop(i)
                return True
        return False

    @staticmethod
    def has_municipalities(province_id):
        """
        Verifica se a província tem municípios associados.

        Args:
            province_id (int): ID da província

        Returns:
            int: Número de municípios associados
        """
        from src.models.municipality import MUNICIPALITIES

        count = sum(1 for m in MUNICIPALITIES if m["provincia_id"] == province_id)
        return count
