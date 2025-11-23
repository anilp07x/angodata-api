"""
Sistema de auditoria para registrar ações importantes na API.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt_identity, get_jwt


class AuditLogger:
    """Gerenciador de logs de auditoria"""
    
    LOG_DIR = Path(__file__).parent.parent.parent / 'logs'
    AUDIT_FILE = LOG_DIR / 'audit.log'
    
    @classmethod
    def ensure_log_dir(cls):
        """Garante que o diretório de logs existe"""
        cls.LOG_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def log_action(cls, action, resource_type, resource_id=None, details=None, user_id=None, user_email=None):
        """
        Registra uma ação no log de auditoria.
        
        Args:
            action (str): Tipo de ação (CREATE, UPDATE, DELETE, LOGIN, etc.)
            resource_type (str): Tipo de recurso afetado (province, user, etc.)
            resource_id: ID do recurso afetado
            details (dict): Detalhes adicionais da ação
            user_id: ID do usuário que executou a ação
            user_email: Email do usuário
        """
        cls.ensure_log_dir()
        
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'user_id': user_id,
            'user_email': user_email,
            'ip_address': request.remote_addr if request else None,
            'user_agent': request.headers.get('User-Agent') if request else None,
            'details': details
        }
        
        try:
            with open(cls.AUDIT_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Erro ao gravar log de auditoria: {e}")
    
    @classmethod
    def get_logs(cls, limit=100, action=None, resource_type=None, user_id=None):
        """
        Recupera logs de auditoria com filtros opcionais.
        
        Args:
            limit (int): Número máximo de logs a retornar
            action (str): Filtrar por tipo de ação
            resource_type (str): Filtrar por tipo de recurso
            user_id: Filtrar por ID do usuário
            
        Returns:
            list: Lista de logs de auditoria
        """
        if not cls.AUDIT_FILE.exists():
            return []
        
        logs = []
        try:
            with open(cls.AUDIT_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log = json.loads(line.strip())
                        
                        # Aplicar filtros
                        if action and log.get('action') != action:
                            continue
                        if resource_type and log.get('resource_type') != resource_type:
                            continue
                        if user_id and log.get('user_id') != user_id:
                            continue
                        
                        logs.append(log)
                        
                        if len(logs) >= limit:
                            break
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Erro ao ler logs de auditoria: {e}")
        
        return list(reversed(logs))  # Mais recentes primeiro


def audit_log(action, resource_type):
    """
    Decorator para registrar automaticamente ações em logs de auditoria.
    
    Args:
        action (str): Tipo de ação (CREATE, UPDATE, DELETE)
        resource_type (str): Tipo de recurso (province, municipality, etc.)
        
    Exemplo:
        @audit_log('CREATE', 'province')
        def create_province():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Obter informações do usuário autenticado
            try:
                user_id = get_jwt_identity()
                claims = get_jwt()
                user_email = claims.get('email')
            except:
                user_id = None
                user_email = None
            
            # Executar a função original
            result = fn(*args, **kwargs)
            
            # Extrair resource_id dos kwargs ou do resultado
            resource_id = kwargs.get('id') or kwargs.get('province_id') or \
                         kwargs.get('municipality_id') or kwargs.get('school_id') or \
                         kwargs.get('market_id') or kwargs.get('hospital_id')
            
            # Tentar extrair resource_id do resultado se for um tuple (response, status_code)
            details = None
            if isinstance(result, tuple) and len(result) >= 1:
                try:
                    response_data = result[0].get_json() if hasattr(result[0], 'get_json') else None
                    if response_data and isinstance(response_data, dict):
                        if 'data' in response_data and isinstance(response_data['data'], dict):
                            resource_id = response_data['data'].get('id', resource_id)
                            details = {'nome': response_data['data'].get('nome')}
                except:
                    pass
            
            # Registrar no log de auditoria
            AuditLogger.log_action(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                user_id=user_id,
                user_email=user_email
            )
            
            return result
        return wrapper
    return decorator
