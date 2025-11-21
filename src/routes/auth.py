"""
Rotas para autenticação e autorização.
Blueprint que gerencia registro, login e gestão de usuários.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from marshmallow import ValidationError
from src.services.auth_service import AuthService
from src.schemas.user_schema import (
    UserRegistrationSchema,
    UserLoginSchema,
    UserResponseSchema
)

# Criação do Blueprint para autenticação
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Instâncias dos schemas
registration_schema = UserRegistrationSchema()
login_schema = UserLoginSchema()
user_response_schema = UserResponseSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    POST /auth/register
    Registra um novo usuário no sistema.
    """
    try:
        data = registration_schema.load(request.get_json())
        
        new_user = AuthService.register(data)
        
        if new_user:
            return jsonify({
                "success": True,
                "message": "Usuário registrado com sucesso",
                "data": new_user
            }), 201
        else:
            # Verificar qual campo está duplicado
            if AuthService.get_user_by_email(data['email']):
                return jsonify({
                    "success": False,
                    "message": "Email já está em uso"
                }), 400
            elif AuthService.get_user_by_username(data['username']):
                return jsonify({
                    "success": False,
                    "message": "Username já está em uso"
                }), 400
            else:
                return jsonify({
                    "success": False,
                    "message": "Erro ao registrar usuário"
                }), 400
                
    except ValidationError as err:
        return jsonify({
            "success": False,
            "message": "Erro de validação",
            "errors": err.messages
        }), 422
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao registrar usuário: {str(e)}"
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    POST /auth/login
    Autentica um usuário e retorna tokens JWT.
    """
    try:
        data = login_schema.load(request.get_json())
        
        user = AuthService.authenticate(data['email'], data['password'])
        
        if user:
            # Criar tokens JWT - identity deve ser string
            access_token = create_access_token(
                identity=str(user['id']),
                additional_claims={
                    'email': user['email'],
                    'username': user['username'],
                    'role': user['role']
                }
            )
            refresh_token = create_refresh_token(identity=str(user['id']))
            
            return jsonify({
                "success": True,
                "message": "Login realizado com sucesso",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Credenciais inválidas"
            }), 401
            
    except ValidationError as err:
        return jsonify({
            "success": False,
            "message": "Erro de validação",
            "errors": err.messages
        }), 422
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao fazer login: {str(e)}"
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    POST /auth/refresh
    Renova o access token usando um refresh token válido.
    """
    try:
        current_user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(current_user_id)
        
        if user:
            # Criar novo access token
            access_token = create_access_token(
                identity=user['id'],
                additional_claims={
                    'email': user['email'],
                    'username': user['username'],
                    'role': user['role']
                }
            )
            
            return jsonify({
                "success": True,
                "data": {
                    "access_token": access_token
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Usuário não encontrado"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao renovar token: {str(e)}"
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    GET /auth/me
    Retorna informações do usuário autenticado.
    """
    try:
        current_user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(current_user_id)
        
        if user:
            return jsonify({
                "success": True,
                "data": user
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Usuário não encontrado"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao buscar usuário: {str(e)}"
        }), 500


@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """
    GET /auth/users
    Lista todos os usuários (apenas para admins).
    """
    try:
        # Verificar se usuário é admin
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({
                "success": False,
                "message": "Acesso negado. Permissões insuficientes"
            }), 403
        
        users = AuthService.get_all_users()
        
        return jsonify({
            "success": True,
            "total": len(users),
            "data": users
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao listar usuários: {str(e)}"
        }), 500
