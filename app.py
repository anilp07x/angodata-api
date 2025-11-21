"""
AngoData API - Ponto de entrada principal da aplicação.
Inicializa e executa o servidor Flask usando o padrão Factory.
"""

from src import create_app

# Criar instância da aplicação usando a factory function
# Por padrão, usa configuração de desenvolvimento
app = create_app('development')

if __name__ == "__main__":
    # Executar o servidor Flask em modo debug
    # Host 0.0.0.0 permite acesso de qualquer IP (útil para deploy)
    # Port 5000 é a porta padrão do Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
