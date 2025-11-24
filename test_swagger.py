"""
Teste simples do Swagger para debug.
"""

from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# Criar API com Swagger
api = Api(
    app,
    version='1.0',
    title='Test API',
    description='API de teste',
    doc='/docs'
)

# Namespace de teste
ns = api.namespace('test', description='Operações de teste')

# Model de exemplo
test_model = api.model('Test', {
    'id': fields.Integer(required=True, description='ID'),
    'message': fields.String(required=True, description='Mensagem')
})

@ns.route('/hello')
class HelloWorld(Resource):
    @ns.doc('get_hello')
    @ns.marshal_with(test_model)
    def get(self):
        """Retorna uma mensagem de teste"""
        return {'id': 1, 'message': 'Hello World!'}

if __name__ == '__main__':
    print("Servidor rodando em http://localhost:5001/docs")
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
