"""
Utilitários de segurança para sanitização e validação de entrada.
"""

import html
import re
from functools import wraps

from flask import jsonify, request


class SecurityValidator:
    """Validador de segurança para entrada de dados"""

    # Padrões suspeitos para SQL Injection
    SQL_INJECTION_PATTERNS = [
        r"(\bOR\b|\bAND\b).*=.*",
        r"(--|#|/\*|\*/)",
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bDROP\b.*\bTABLE\b)",
        r"(\bINSERT\b.*\bINTO\b)",
        r"(\bDELETE\b.*\bFROM\b)",
        r"(\bUPDATE\b.*\bSET\b)",
        r"(;.*\b(DROP|DELETE|INSERT|UPDATE)\b)",
    ]

    # Padrões suspeitos para XSS
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe",
        r"<embed",
        r"<object",
    ]

    @classmethod
    def sanitize_string(cls, value):
        """
        Sanitiza uma string removendo caracteres HTML perigosos.

        Args:
            value (str): String a ser sanitizada

        Returns:
            str: String sanitizada
        """
        if not isinstance(value, str):
            return value

        # Escape HTML
        sanitized = html.escape(value)

        # Remover caracteres de controle
        sanitized = "".join(char for char in sanitized if ord(char) >= 32 or char in "\n\r\t")

        return sanitized

    @classmethod
    def check_sql_injection(cls, value):
        """
        Verifica se uma string contém padrões suspeitos de SQL Injection.

        Args:
            value (str): String a ser verificada

        Returns:
            bool: True se suspeito, False caso contrário
        """
        if not isinstance(value, str):
            return False

        value_upper = value.upper()

        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value_upper, re.IGNORECASE):
                return True

        return False

    @classmethod
    def check_xss(cls, value):
        """
        Verifica se uma string contém padrões suspeitos de XSS.

        Args:
            value (str): String a ser verificada

        Returns:
            bool: True se suspeito, False caso contrário
        """
        if not isinstance(value, str):
            return False

        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return True

        return False

    @classmethod
    def sanitize_dict(cls, data):
        """
        Sanitiza recursivamente todos os valores string em um dicionário.

        Args:
            data (dict): Dicionário a ser sanitizado

        Returns:
            dict: Dicionário sanitizado
        """
        if not isinstance(data, dict):
            return data

        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = cls.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = cls.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    (
                        cls.sanitize_string(item)
                        if isinstance(item, str)
                        else cls.sanitize_dict(item) if isinstance(item, dict) else item
                    )
                    for item in value
                ]
            else:
                sanitized[key] = value

        return sanitized

    @classmethod
    def validate_input(cls, data):
        """
        Valida entrada de dados procurando por padrões suspeitos.

        Args:
            data (dict): Dados a serem validados

        Returns:
            tuple: (is_valid, error_message)
        """
        if not isinstance(data, dict):
            return True, None

        for key, value in data.items():
            if isinstance(value, str):
                if cls.check_sql_injection(value):
                    return False, f"Entrada suspeita detectada no campo '{key}': possível SQL Injection"

                if cls.check_xss(value):
                    return False, f"Entrada suspeita detectada no campo '{key}': possível XSS"

            elif isinstance(value, dict):
                is_valid, error = cls.validate_input(value)
                if not is_valid:
                    return is_valid, error

        return True, None


def sanitize_input():
    """
    Decorator para sanitizar automaticamente entrada de dados JSON.
    Deve ser aplicado antes da validação com schemas.

    Exemplo:
        @app.route('/endpoint', methods=['POST'])
        @sanitize_input()
        def create_resource():
            data = request.get_json()
            # data já está sanitizado
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.is_json:
                try:
                    data = request.get_json()

                    # Validar entrada
                    is_valid, error = SecurityValidator.validate_input(data)
                    if not is_valid:
                        return jsonify({"success": False, "message": error}), 400

                    # Sanitizar dados
                    sanitized_data = SecurityValidator.sanitize_dict(data)

                    # Substituir dados originais pelos sanitizados
                    request._cached_json = (sanitized_data, sanitized_data)

                except Exception as e:
                    return jsonify({"success": False, "message": f"Erro ao processar entrada: {str(e)}"}), 400

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def add_security_headers(response):
    """
    Adiciona headers de segurança às respostas HTTP.

    Args:
        response: Objeto de resposta Flask

    Returns:
        response: Resposta com headers de segurança adicionados
    """
    from flask import request

    # Prevenir clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # Prevenir MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # XSS Protection (legacy, mas ainda útil)
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Content Security Policy - Relaxar para Swagger UI
    if request.path.startswith("/api/docs") or request.path.startswith("/swaggerui"):
        # Swagger UI precisa de 'unsafe-inline' e 'unsafe-eval' para JavaScript
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self' data:"
        )
    else:
        # CSP restritivo para outras rotas
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"

    # Strict Transport Security (HSTS) - apenas em produção com HTTPS
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Permissions Policy
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response
