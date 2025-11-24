"""
Serviço de lógica de negócio para Escolas.
Responsável por buscar e manipular dados de escolas.
"""

from src.models.school import SCHOOLS
from src.utils.persistence import persist_data


class SchoolService:
    """Serviço para operações com escolas."""

    @staticmethod
    def get_all():
        """Retorna todas as escolas."""
        return SCHOOLS

    @staticmethod
    def get_by_id(school_id):
        """
        Retorna uma escola específica por ID.

        Args:
            school_id (int): ID da escola

        Returns:
            dict ou None: Dados da escola ou None se não encontrada
        """
        school_id = int(school_id)
        for school in SCHOOLS:
            if school["id"] == school_id:
                return school
        return None

    @staticmethod
    def get_by_province(province_id):
        """
        Retorna todas as escolas de uma província específica.

        Args:
            province_id (int): ID da província

        Returns:
            list: Lista de escolas da província
        """
        province_id = int(province_id)
        return [s for s in SCHOOLS if s["provincia_id"] == province_id]

    @staticmethod
    def get_by_municipality(municipality_id):
        """
        Retorna todas as escolas de um município específico.

        Args:
            municipality_id (int): ID do município

        Returns:
            list: Lista de escolas do município
        """
        municipality_id = int(municipality_id)
        return [s for s in SCHOOLS if s.get("municipio_id") == municipality_id]

    @staticmethod
    def create(data):
        """
        Cria uma nova escola.

        Args:
            data (dict): Dados da escola

        Returns:
            dict ou None: Escola criada ou None se validação falhar
        """
        from src.services.municipality_service import MunicipalityService
        from src.services.province_service import ProvinceService

        # Validar província
        province = ProvinceService.get_by_id(data["provincia_id"])
        if not province:
            return None

        # Validar município
        municipality = MunicipalityService.get_by_id(data["municipio_id"])
        if not municipality:
            return None

        # Validar se município pertence à província
        if municipality["provincia_id"] != data["provincia_id"]:
            return None

        # Gerar novo ID
        new_id = max([s["id"] for s in SCHOOLS]) + 1 if SCHOOLS else 1

        new_school = {
            "id": new_id,
            "nome": data["nome"],
            "tipo": data["tipo"],
            "provincia_id": data["provincia_id"],
            "provincia_nome": province["nome"],
            "municipio_id": data["municipio_id"],
            "municipio": municipality["nome"],
            "endereco": data["endereco"],
        }

        SCHOOLS.append(new_school)
        return new_school

    @staticmethod
    @persist_data
    def update(school_id, data):
        """
        Atualiza uma escola existente.

        Args:
            school_id (int): ID da escola
            data (dict): Dados para atualizar

        Returns:
            dict ou None: Escola atualizada ou None se não encontrada/validação falhar
        """
        from src.services.municipality_service import MunicipalityService
        from src.services.province_service import ProvinceService

        school_id = int(school_id)
        for school in SCHOOLS:
            if school["id"] == school_id:
                # Atualizar campos simples
                if "nome" in data:
                    school["nome"] = data["nome"]
                if "tipo" in data:
                    school["tipo"] = data["tipo"]
                if "endereco" in data:
                    school["endereco"] = data["endereco"]

                # Atualizar província/município (validar relacionamento)
                if "provincia_id" in data or "municipio_id" in data:
                    provincia_id = data.get("provincia_id", school["provincia_id"])
                    municipio_id = data.get("municipio_id", school["municipio_id"])

                    # Validar província
                    province = ProvinceService.get_by_id(provincia_id)
                    if not province:
                        return None

                    # Validar município
                    municipality = MunicipalityService.get_by_id(municipio_id)
                    if not municipality:
                        return None

                    # Validar relacionamento
                    if municipality["provincia_id"] != provincia_id:
                        return None

                    school["provincia_id"] = provincia_id
                    school["provincia_nome"] = province["nome"]
                    school["municipio_id"] = municipio_id
                    school["municipio"] = municipality["nome"]

                return school
        return None

    @staticmethod
    @persist_data
    def delete(school_id):
        """
        Deleta uma escola.

        Args:
            school_id (int): ID da escola

        Returns:
            bool: True se deletado, False se não encontrado
        """
        school_id = int(school_id)
        for i, school in enumerate(SCHOOLS):
            if school["id"] == school_id:
                SCHOOLS.pop(i)
                return True
        return False
