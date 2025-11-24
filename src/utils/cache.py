"""
Sistema de cache com Redis.
"""

import functools
import json
import os
from typing import Any, Callable, Optional

from flask_caching import Cache

# Configuração do cache
cache_config = {
    "CACHE_TYPE": "redis" if os.getenv("USE_REDIS", "False").lower() == "true" else "SimpleCache",
    "CACHE_REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    "CACHE_DEFAULT_TIMEOUT": 300,  # 5 minutos
    "CACHE_KEY_PREFIX": "angodata_",
}

# Instância global do cache
cache = Cache()


def init_cache(app):
    """
    Inicializa o cache na aplicação Flask.

    Args:
        app: Instância Flask
    """
    # Desabilitar cache em modo de teste
    if app.config.get("TESTING", False):
        app.config["CACHE_TYPE"] = "null"
        cache.init_app(app)
        print("✓ Cache desabilitado (Testing mode)")
        return

    app.config.from_mapping(cache_config)
    cache.init_app(app)

    cache_type = "Redis" if cache_config["CACHE_TYPE"] == "redis" else "Memory"
    print(f"✓ Cache inicializado ({cache_type})")


def cache_key_from_request(*args, **kwargs):
    """
    Gera chave de cache baseada na URL e query params.

    Returns:
        str: Chave única para o cache
    """
    from flask import request

    # Incluir path, query params e se está usando database
    use_db = os.getenv("USE_DATABASE", "False").lower() == "true"
    db_suffix = "_db" if use_db else "_json"

    # Criar chave a partir da URL e query string
    key = f"{request.path}{db_suffix}?{request.query_string.decode('utf-8')}"
    return key


def cached_route(timeout: int = 300):
    """
    Decorator para cachear responses de routes.

    Args:
        timeout: Tempo em segundos (padrão: 5 minutos)

    Usage:
        @cached_route(timeout=600)
        def get_provinces():
            ...
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Gerar chave de cache
            cache_key = cache_key_from_request()

            # Tentar pegar do cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response

            # Executar função
            response = f(*args, **kwargs)

            # Salvar no cache
            cache.set(cache_key, response, timeout=timeout)

            return response

        return decorated_function

    return decorator


def cache_service_result(timeout: int = 300, key_prefix: str = ""):
    """
    Decorator para cachear resultados de funções de service.

    Args:
        timeout: Tempo em segundos
        key_prefix: Prefixo para a chave

    Usage:
        @cache_service_result(timeout=600, key_prefix='provinces')
        def get_all():
            ...
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Gerar chave baseada em função, args e kwargs
            use_db = os.getenv("USE_DATABASE", "False").lower() == "true"
            db_suffix = "_db" if use_db else "_json"

            args_str = "_".join(str(arg) for arg in args)
            kwargs_str = "_".join(f"{k}_{v}" for k, v in sorted(kwargs.items()))

            cache_key = f"{key_prefix}_{f.__name__}_{args_str}_{kwargs_str}{db_suffix}"

            # Tentar pegar do cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Executar função
            result = f(*args, **kwargs)

            # Salvar no cache
            cache.set(cache_key, result, timeout=timeout)

            return result

        return decorated_function

    return decorator


def invalidate_cache_pattern(pattern: str):
    """
    Invalida todos os caches que correspondem ao padrão.

    Args:
        pattern: Padrão de chave (ex: 'provinces_*')
    """
    try:
        if cache_config["CACHE_TYPE"] == "redis":
            # Para Redis, usar SCAN para encontrar e deletar chaves
            redis_client = cache.cache._write_client
            prefix = cache_config["CACHE_KEY_PREFIX"]
            full_pattern = f"{prefix}{pattern}"

            keys = []
            cursor = 0
            while True:
                cursor, partial_keys = redis_client.scan(cursor, match=full_pattern, count=100)
                keys.extend(partial_keys)
                if cursor == 0:
                    break

            if keys:
                redis_client.delete(*keys)
                print(f"✓ Cache invalidado: {len(keys)} chaves ({pattern})")
        else:
            # Para SimpleCache, limpar tudo
            cache.clear()
            print(f"✓ Cache limpo (SimpleCache)")
    except Exception as e:
        print(f"✗ Erro ao invalidar cache: {e}")


def invalidate_entity_cache(entity_name: str):
    """
    Invalida cache de uma entidade específica.

    Args:
        entity_name: Nome da entidade (provinces, municipalities, etc)
    """
    patterns = [
        f"{entity_name}_*",
        f"*/{entity_name}/*",
    ]

    for pattern in patterns:
        invalidate_cache_pattern(pattern)


class CacheManager:
    """Gerenciador de cache para operações comuns."""

    @staticmethod
    def clear_all():
        """Limpa todo o cache."""
        cache.clear()
        print("✓ Todo o cache foi limpo")

    @staticmethod
    def get_stats() -> dict:
        """
        Retorna estatísticas do cache.

        Returns:
            dict: Estatísticas de uso
        """
        try:
            if cache_config["CACHE_TYPE"] == "redis":
                redis_client = cache.cache._write_client
                info = redis_client.info("stats")

                return {
                    "type": "Redis",
                    "keyspace_hits": info.get("keyspace_hits", 0),
                    "keyspace_misses": info.get("keyspace_misses", 0),
                    "total_commands": info.get("total_commands_processed", 0),
                    "connected": redis_client.ping(),
                }
            else:
                return {"type": "SimpleCache (Memory)", "note": "Estatísticas detalhadas disponíveis apenas com Redis"}
        except Exception as e:
            return {"type": "Unknown", "error": str(e)}

    @staticmethod
    def warmup_cache():
        """
        Aquece o cache com dados frequentemente acessados.
        Executar no startup da aplicação.
        """
        print("🔥 Aquecendo cache...")

        # Verificar se deve usar database
        use_db = os.getenv("USE_DATABASE", "False").lower() == "true"

        if use_db:
            from src.services.db.province_service_db import ProvinceServiceDB

            ProvinceServiceDB.get_all()
        else:
            from src.services.province_service import ProvinceService

            ProvinceService.get_all()

        print("✓ Cache aquecido com dados de províncias")
