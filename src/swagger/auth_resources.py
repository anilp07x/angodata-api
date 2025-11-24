"""
Recursos Swagger para Autenticação.
Documentação dos endpoints de auth.
"""

from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.swagger.auth_ns import (
    auth_ns,
    login_model,
    register_model,
    change_password_model,
    token_response,
    user_response,
    success_response,
    error_response
)
from src.services.auth_service import AuthService
from marshmallow import ValidationError


@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.doc('login')
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login bem-sucedido', token_response)
    @auth_ns.response(401, 'Credenciais inválidas', error_response)
    @auth_ns.response(400, 'Dados inválidos', error_response)
    def post(self):
        """Autentica usuário e retorna token JWT"""
        data = request.json
        
        if not data or 'email' not in data or 'password' not in data:
            return {
                'success': False,
                'message': 'Email e senha são obrigatórios'
            }, 400
        
        user = AuthService.authenticate(data['email'], data['password'])
        
        if not user:
            return {
                'success': False,
                'message': 'Credenciais inválidas'
            }, 401
        
        from flask_jwt_extended import create_access_token
        access_token = create_access_token(identity=user['id'])
        
        return {
            'access_token': access_token,
            'user': user
        }, 200


@auth_ns.route('/register')
class RegisterResource(Resource):
    @auth_ns.doc('register')
    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'Usuário criado com sucesso', user_response)
    @auth_ns.response(400, 'Dados inválidos ou email já existe', error_response)
    def post(self):
        """Registra novo usuário no sistema"""
        data = request.json
        
        if not data or 'email' not in data or 'password' not in data or 'nome' not in data:
            return {
                'success': False,
                'message': 'Email, senha e nome são obrigatórios'
            }, 400
        
        user_data = {
            'email': data['email'],
            'password': data['password'],
            'username': data['nome'],
            'role': data.get('role', 'user')
        }
        
        user = AuthService.register(user_data)
        
        if not user:
            return {
                'success': False,
                'message': 'Email ou nome de usuário já existe'
            }, 400
        
        return {
            'success': True,
            'message': 'Usuário criado com sucesso',
            'data': user
        }, 201


@auth_ns.route('/me')
class MeResource(Resource):
    @auth_ns.doc('get_current_user', security='Bearer')
    @auth_ns.response(200, 'Informações do usuário', user_response)
    @auth_ns.response(401, 'Não autorizado', error_response)
    @auth_ns.response(404, 'Usuário não encontrado', error_response)
    @jwt_required()
    def get(self):
        """Retorna informações do usuário autenticado"""
        user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(user_id)
        
        if not user:
            return {
                'success': False,
                'message': 'Usuário não encontrado'
            }, 404
        
        return {
            'success': True,
            'data': user
        }, 200


@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @auth_ns.doc('refresh_token', security='Bearer')
    @auth_ns.response(200, 'Token renovado', token_response)
    @auth_ns.response(401, 'Token inválido', error_response)
    @jwt_required()
    def post(self):
        """Renova o token JWT (refresh token)"""
        user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(user_id)
        
        if not user:
            return {
                'success': False,
                'message': 'Usuário não encontrado'
            }, 401
        
        from flask_jwt_extended import create_access_token
        access_token = create_access_token(identity=user['id'])
        
        return {
            'access_token': access_token,
            'user': user
        }, 200


@auth_ns.route('/change-password')
class ChangePasswordResource(Resource):
    @auth_ns.doc('change_password', security='Bearer')
    @auth_ns.expect(change_password_model)
    @auth_ns.response(200, 'Senha alterada com sucesso', success_response)
    @auth_ns.response(400, 'Dados inválidos', error_response)
    @auth_ns.response(401, 'Senha atual incorreta', error_response)
    @jwt_required()
    def put(self):
        """Altera a senha do usuário autenticado"""
        user_id = get_jwt_identity()
        data = request.json
        
        if not data or 'current_password' not in data or 'new_password' not in data:
            return {
                'success': False,
                'message': 'Senha atual e nova senha são obrigatórias'
            }, 400
        
        user = AuthService.get_user_by_id(user_id)
        if not user:
            return {
                'success': False,
                'message': 'Usuário não encontrado'
            }, 401
        
        # Verificar senha atual
        full_user = AuthService.get_user_by_email(user['email'])
        if not full_user:
            return {
                'success': False,
                'message': 'Usuário não encontrado'
            }, 401
        
        if not AuthService.verify_password(full_user['password_hash'], data['current_password']):
            return {
                'success': False,
                'message': 'Senha atual incorreta'
            }, 401
        
        # Atualizar senha
        updated = AuthService.update_user(user_id, {'password': data['new_password']})
        
        if not updated:
            return {
                'success': False,
                'message': 'Erro ao atualizar senha'
            }, 400
        
        return {
            'success': True,
            'message': 'Senha alterada com sucesso'
        }, 200


@auth_ns.route('/users')
class UserListResource(Resource):
    @auth_ns.doc('list_users', security='Bearer')
    @auth_ns.response(200, 'Lista de usuários', success_response)
    @auth_ns.response(401, 'Não autorizado', error_response)
    @auth_ns.response(403, 'Sem permissão (apenas Admin)', error_response)
    @jwt_required()
    def get(self):
        """Lista todos os usuários (apenas Admin)"""
        users = AuthService.get_all_users()
        
        return {
            'success': True,
            'total': len(users),
            'data': users
        }, 200
