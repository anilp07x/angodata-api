"""
Utilitários compartilhados entre os services DB.
"""

from typing import Optional, Tuple

from src.database.models import Municipality, Province


def resolve_location(
    session, provincia_id: int, municipio_id: Optional[int]
) -> Optional[Tuple[str, Optional[int], Optional[str]]]:
    """
    Valida província e município (existência + vínculo) e retorna
    (provincia_nome, municipio_id, municipio_nome).

    Retorna None se alguma validação falhar.
    """
    provincia = session.query(Province).filter(Province.id == provincia_id).first()
    if not provincia:
        return None

    if municipio_id is None:
        return (provincia.nome, None, None)

    municipio = (
        session.query(Municipality).filter(Municipality.id == municipio_id).first()
    )
    if not municipio:
        return None

    # Validar se município pertence à província
    if municipio.provincia_id != provincia_id:
        return None

    return (provincia.nome, municipio_id, municipio.nome)
