# AngoData API 🇦🇴

API REST em Flask que fornece dados públicos de Angola (províncias, municípios, escolas, mercados e hospitais).

## 📋 Características

- ✅ Arquitetura modular com separação de responsabilidades
- ✅ Padrão Factory para inicialização da aplicação
- ✅ Blueprints para organização de rotas
- ✅ CORS habilitado para integração front-end
- ✅ Dados em memória (preparado para migração para BD)
- ✅ Respostas JSON padronizadas em português

## 🚀 Como Executar

### 1. Ativar o Virtual Environment
```bash
source venv/bin/activate
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar a Aplicação
```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## 📡 Endpoints Disponíveis

### Home
- `GET /` - Informações sobre a API e endpoints disponíveis

### Províncias
- `GET /provinces/all` - Lista todas as 18 províncias de Angola
- `GET /provinces/<id>` - Detalhes de uma província específica

### Municípios
- `GET /municipalities/all` - Lista todos os municípios
- `GET /municipalities/<id>` - Detalhes de um município específico

### Escolas
- `GET /schools/all` - Lista todas as escolas
- `GET /schools/<id>` - Detalhes de uma escola específica

### Mercados
- `GET /markets/all` - Lista todos os mercados
- `GET /markets/<id>` - Detalhes de um mercado específico

### Hospitais
- `GET /hospitals/all` - Lista todos os hospitais
- `GET /hospitals/<id>` - Detalhes de um hospital específico

## 📂 Estrutura do Projeto

```
angodata-api/
├── app.py                      # Ponto de entrada
├── requirements.txt            # Dependências
├── src/
│   ├── __init__.py            # Factory create_app()
│   ├── config/                # Configurações
│   ├── models/                # Dados in-memory
│   ├── services/              # Lógica de negócio
│   ├── routes/                # Blueprints (endpoints)
│   └── database/              # Futuro: integração com BD
└── venv/                      # Virtual environment
```

## 🧪 Testar a API

### Usando curl
```bash
# Endpoint principal
curl http://localhost:5000/

# Listar províncias
curl http://localhost:5000/provinces/all

# Província específica (Luanda)
curl http://localhost:5000/provinces/1
```

### Usando navegador
- Acesse `http://localhost:5000/` para ver a documentação básica
- Acesse `http://localhost:5000/provinces/all` para ver todas as províncias

## 🛠️ Tecnologias

- **Python** 3.12.3
- **Flask** 3.1.2
- **Flask-CORS** 5.0.0

## 📚 Padrões de Arquitetura

### Factory Pattern
Aplicação inicializada com `create_app()` permitindo diferentes configurações.

### Three-Layer Architecture
1. **Routes**: Recebem requests HTTP
2. **Services**: Contêm lógica de negócio
3. **Models**: Estruturas de dados

### Blueprints
Cada entidade (províncias, municípios, etc.) tem seu próprio Blueprint modular.

## 🔮 Roadmap Futuro

- [ ] Migração para PostgreSQL com SQLAlchemy
- [ ] Autenticação JWT
- [ ] Paginação de resultados
- [ ] Filtros e busca avançada
- [ ] Testes unitários e de integração
- [ ] Documentação OpenAPI/Swagger
- [ ] Deploy em produção

## 📄 Formato de Resposta

### Sucesso
```json
{
    "success": true,
    "total": 18,
    "data": [...]
}
```

### Erro
```json
{
    "success": false,
    "message": "Descrição do erro"
}
```

## 🤝 Contribuir

Este projeto está em desenvolvimento ativo. Sugestões e contribuições são bem-vindas!

## 📝 Licença

Este projeto fornece dados públicos de Angola de forma aberta.
