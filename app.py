"""
AngoData API - Ponto de entrada principal da aplicação.
Inicializa e executa o servidor Flask usando o padrão Factory.
"""

import os

from dotenv import load_dotenv
from src import create_app

# Carregar variáveis de ambiente
load_dotenv()

# Configuração via ambiente (FLASK_ENV=development|production)
config_name = os.getenv("FLASK_ENV", "development")

app = create_app(config_name)

if __name__ == "__main__":
    # Porta via ambiente (Render define PORT); 5001 local (porta 5000 em uso)
    port = int(os.getenv("PORT", 5001))
    debug = app.config.get("DEBUG", False)
    app.run(host="0.0.0.0", port=port, debug=debug)
