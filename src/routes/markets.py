"""
Rotas para operações com Mercados.
Blueprint que gerencia endpoints relacionados a mercados de Angola.
"""

from flask import Blueprint, jsonify
from src.services.market_service import MarketService

# Criação do Blueprint para mercados
markets_bp = Blueprint('markets', __name__, url_prefix='/markets')


@markets_bp.route('/all', methods=['GET'])
def get_all_markets():
    """
    GET /markets/all
    Retorna todos os mercados de Angola.
    """
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
