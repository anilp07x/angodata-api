"""
Utilitários para persistência de dados
"""

from functools import wraps

from src.database.json_storage import JSONStorage


def persist_data(func):
    """
    Decorator que salva dados em JSON após a execução de uma função.
    Útil para operações de CREATE, UPDATE e DELETE.

    Usage:
        @persist_data
        def create_province(data):
            # ... código ...
            return new_province
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Executar função original
        result = func(*args, **kwargs)

        # Se a operação foi bem-sucedida, salvar dados
        if result is not None and result is not False:
            JSONStorage.save_all_entities()

        return result

    return wrapper
