"""
Rotas para operações com Mercados.
Blueprint que gerencia endpoints relacionados a mercados de Angola.
"""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.services.market_service import MarketService
from src.schemas.market_schema import MarketSchema

# Criação do Blueprint para mercados
markets_bp = Blueprint('markets', __name__, url_prefix='/markets')

# Instância do schema
market_schema = MarketSchema()


@markets_bp.route('/all', methods=['GET'])
def get_all_markets():
    """
    GET /markets/all
    Retorna todos os mercados de Angola.
    Aceita query parameters: ?provincia_id=<id> ou ?municipio_id=<id>
    """
    provincia_id = request.args.get('provincia_id', type=int)
    municipio_id = request.args.get('municipio_id', type=int)
    
    if municipio_id:
        markets = MarketService.get_by_municipality(municipio_id)
    elif provincia_id:
        markets = MarketService.get_by_province(provincia_id)
    else:
        markets = MarketService.get_all()
    
    return jsonify({
        "success": True,
        "total": len(markets),
        "data": markets
    }), 200


@markets_bp.route('/<int:market_id>', methods=['GET'])
def get_market_by_id(market_id):
    """
    GET /markets/<id>
    Retorna um mercado específico por ID.
    """
    market = MarketService.get_by_id(market_id)
    
    if market:
        return jsonify({
            "success": True,
            "data": market
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": f"Mercado com ID {market_id} não encontrado"
        }), 404


@markets_bp.route('', methods=['POST'])
def create_market():
    """
    POST /markets
    Cria um novo mercado.
    """
    try:
        data = market_schema.load(request.get_json())
        
        new_market = MarketService.create(data)
        
        if new_market:
            return jsonify({
                "success": True,
                "message": "Mercado criado com sucesso",
                "data": new_market
            }), 201
        else:
            return jsonify({
                "success": False,
                "message": "Município não pertence à província especificada"
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
            "message": f"Erro ao criar mercado: {str(e)}"
        }), 500


@markets_bp.route('/<int:market_id>', methods=['PUT'])
def update_market(market_id):
    """
    PUT /markets/<id>
    Atualiza um mercado existente.
    """
    try:
        data = market_schema.load(request.get_json(), partial=True)
        
        updated_market = MarketService.update(market_id, data)
        
        if updated_market:
            return jsonify({
                "success": True,
                "message": "Mercado atualizado com sucesso",
                "data": updated_market
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Mercado não encontrado ou município não pertence à província especificada"
            }), 404
            
    except ValidationError as err:
        return jsonify({
            "success": False,
            "message": "Erro de validação",
            "errors": err.messages
        }), 422
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao atualizar mercado: {str(e)}"
        }), 500


@markets_bp.route('/<int:market_id>', methods=['DELETE'])
def delete_market(market_id):
    """
    DELETE /markets/<id>
    Deleta um mercado.
    """
    try:
        deleted = MarketService.delete(market_id)
        
        if deleted:
            return jsonify({
                "success": True,
                "message": "Mercado deletado com sucesso"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": f"Mercado com ID {market_id} não encontrado"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao deletar mercado: {str(e)}"
        }), 500
