"""
Decoradores customizados para autorização e controle de acesso.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def role_required(allowed_roles):
    """
    Decorator para verificar se o usuário tem uma das roles permitidas.
    Deve ser usado junto com @jwt_required().
    
    Args:
        allowed_roles (list): Lista de roles permitidas ['admin', 'editor', 'user']
        
    Exemplo:
        @jwt_required()
        @role_required(['admin', 'editor'])
        def create_resource():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "Acesso negado. Permissões insuficientes"
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required():
    """
    Decorator para verificar se o usuário é administrador.
    Deve ser usado junto com @jwt_required().
    
    Exemplo:
        @jwt_required()
        @admin_required()
        def admin_only_function():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role != 'admin':
                return jsonify({
                    "success": False,
                    "message": "Acesso negado. Apenas administradores podem realizar esta ação"
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def editor_or_admin_required():
    """
    Decorator para verificar se o usuário é editor ou administrador.
    Deve ser usado junto com @jwt_required().
    
    Exemplo:
        @jwt_required()
        @editor_or_admin_required()
        def modify_content():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in ['admin', 'editor']:
                return jsonify({
                    "success": False,
                    "message": "Acesso negado. Apenas editores e administradores podem realizar esta ação"
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
